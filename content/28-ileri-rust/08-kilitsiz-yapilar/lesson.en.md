# Spinlocks and Lock-Free Structures

We learned atomics and `UnsafeCell`. Joining them, we can write our own lock. In this section we first build a **spinlock**, then a lock-free stack.

## The parts

A lock needs two things: an "is it taken?" flag and the protected data.

```rust
use std::cell::UnsafeCell;
use std::sync::atomic::AtomicBool;
use std::thread;

struct SpinLock<T> {
    locked: AtomicBool,
    value: UnsafeCell<T>,
}

fn main() {
    let lock = SpinLock { locked: AtomicBool::new(false), value: UnsafeCell::new(0) };
    thread::scope(|s| {
        s.spawn(|| &lock);
    });
}
```

```text
error[E0277]: `UnsafeCell<{integer}>` cannot be shared between threads safely
  --> main.rs:13:11
   |
13 |         s.spawn(|| &lock);
   |           ^^^^^ `UnsafeCell<{integer}>` cannot be shared between threads safely
   |
   = help: within `SpinLock<{integer}>`, the trait `Sync` is not implemented for
     `UnsafeCell<{integer}>`
note: required because it appears within the type `SpinLock<{integer}>`
  --> main.rs:5:8
   |
 5 | struct SpinLock<T> {
   |        ^^^^^^^^
   = note: required for `&SpinLock<{integer}>` to implement `Send`
note: required by a bound in `Scope::<'scope, 'env>::spawn`
```

The compiler is right: `UnsafeCell` is not `Sync`. Making the promise is up to us, because the flag will order the access.

## A spinlock

```rust
use std::cell::UnsafeCell;
use std::ops::{Deref, DerefMut};
use std::sync::atomic::{AtomicBool, Ordering};
use std::thread;

pub struct SpinLock<T> {
    locked: AtomicBool,
    value: UnsafeCell<T>,
}

// SAFETY: the flag gives one access at a time, so T only needs to be Send.
unsafe impl<T: Send> Sync for SpinLock<T> {}

impl<T> SpinLock<T> {
    pub fn new(value: T) -> Self {
        SpinLock { locked: AtomicBool::new(false), value: UnsafeCell::new(value) }
    }

    pub fn lock(&self) -> Guard<'_, T> {
        while self
            .locked
            .compare_exchange_weak(false, true, Ordering::Acquire, Ordering::Relaxed)
            .is_err()
        {
            std::hint::spin_loop();
        }
        Guard { lock: self }
    }
}

pub struct Guard<'a, T> {
    lock: &'a SpinLock<T>,
}

impl<T> Deref for Guard<'_, T> {
    type Target = T;

    fn deref(&self) -> &T {
        // SAFETY: the guard exists, so this branch holds the lock.
        unsafe { &*self.lock.value.get() }
    }
}

impl<T> DerefMut for Guard<'_, T> {
    fn deref_mut(&mut self) -> &mut T {
        // SAFETY: as above, and &mut self is unique.
        unsafe { &mut *self.lock.value.get() }
    }
}

impl<T> Drop for Guard<'_, T> {
    fn drop(&mut self) {
        self.lock.locked.store(false, Ordering::Release);
    }
}

fn main() {
    let lock = SpinLock::new(0);
    thread::scope(|s| {
        for _ in 0..4 {
            s.spawn(|| {
                for _ in 0..1000 {
                    *lock.lock() += 1;
                }
            });
        }
    });
    println!("{}", *lock.lock());
}
```

```text
4000
```

Each line has a reason:

| Line | Why |
|---|---|
| The `T: Send` condition | The value travels between branches; no `T: Sync` is needed |
| `compare_exchange_weak` | We are in a loop, so a spurious failure is fine |
| `Acquire` | On taking the lock, the previous owner's writes appear |
| `Release` | On releasing the lock, our writes appear |
| `spin_loop` | It tells the processor "I am waiting" |
| `Guard` and `Drop` | The lock cannot be forgotten, and opens in a panic too |
| `&self`, not `&mut self` | A shared value is what gets locked |

This structure gives the same interface as `Mutex`. So why always `Mutex`?

## Why not use a spinlock?

A spinlock spins the processor pointlessly while waiting. `Mutex` tells the operating system "put me to sleep".

| Case | Spinlock | `Mutex` |
|---|---|---|
| Very short work, many cores | Good | Good |
| Long work | A core spins for nothing | It sleeps |
| The holder loses its time slice | Everyone spins | It sleeps |
| Places with no kernel (`no_std`) | May be the only choice | None |

A modern `Mutex` first spins briefly, then sleeps. So in application code a spinlock is almost never the right answer. We wrote it here to see how it works.

## A lock-free stack

A lock-free structure is one where others can progress even if a branch sleeps. The simplest is a linked list whose head is an atomic pointer.

`push`: make the new node's `next` show the old head, then change the head with `compare_exchange`. If another branch stepped in, retry:

```rust
use std::ptr;
use std::sync::atomic::{AtomicPtr, Ordering};
use std::thread;

struct Node<T> {
    value: T,
    next: *mut Node<T>,
}

struct TakeStack<T> {
    head: AtomicPtr<Node<T>>,
}

// SAFETY: values move between branches, and the head is atomic.
unsafe impl<T: Send> Sync for TakeStack<T> {}

impl<T> TakeStack<T> {
    fn new() -> Self {
        TakeStack { head: AtomicPtr::new(ptr::null_mut()) }
    }

    fn push(&self, value: T) {
        let node = Box::into_raw(Box::new(Node { value, next: ptr::null_mut() }));
        let mut head = self.head.load(Ordering::Relaxed);
        loop {
            // SAFETY: the node is not shared yet.
            unsafe { (*node).next = head };
            let result = self.head.compare_exchange_weak(
                head,
                node,
                Ordering::Release,
                Ordering::Relaxed,
            );
            match result {
                Ok(_) => return,
                Err(actual) => head = actual,
            }
        }
    }

    fn take_all(&self) -> Vec<T> {
        let mut current = self.head.swap(ptr::null_mut(), Ordering::Acquire);
        let mut out = Vec::new();
        while !current.is_null() {
            // SAFETY: swap gave the whole chain to this branch alone.
            let node = unsafe { Box::from_raw(current) };
            current = node.next;
            out.push(node.value);
        }
        out
    }
}

impl<T> Drop for TakeStack<T> {
    fn drop(&mut self) {
        self.take_all();
    }
}

fn main() {
    let stack = TakeStack::new();
    thread::scope(|s| {
        for n in 0..4 {
            let stack = &stack;
            s.spawn(move || {
                for i in 0..100 {
                    stack.push(n * 1000 + i);
                }
            });
        }
    });
    let mut all = stack.take_all();
    all.sort();
    println!("{} {} {}", all.len(), all[0], all[399]);
    println!("{}", stack.take_all().len());
}
```

```text
400 0 3099
0
```

`take_all` turns the head to null with `swap` and takes the whole chain in one move. So no one can look at a deleted node.

## Why is pop hard?

"Read the head, take its `next`, make the head `next`" looks easy. There are two real problems:

1. **Freed memory:** another branch may have popped and deleted the node; reading its `next` is undefined behavior.
2. **ABA:** the head is `A`, we read it. Another branch took `A`, took `B`, and put `A` back. `compare_exchange` says "still `A`" and succeeds, but `next` is now wrong.

So real lock-free structures need a memory reclamation scheme (hazard pointers, epochs). Do not write it yourself: use a well-tested crate like `crossbeam`. We chose the `take_all` pattern exactly because it avoids both of these.

## Summary

- A lock: an atomic flag + `UnsafeCell` + `unsafe impl Sync` + `Guard`.
- `Acquire` on taking, `Release` on releasing.
- A spinlock is almost never right in application code; `Mutex`.
- A lock-free `push` is easy; `pop` is hard because of freed memory and ABA.
- For a real lock-free structure, a well-tested crate.
