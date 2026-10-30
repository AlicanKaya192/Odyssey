# Send and Sync

Rust stops data races at compile time because of two small traits. They have no methods and carry only a promise. The compiler gives them to most types by itself, and we write the rest.

## Two promises

| Trait | Its promise | A counterexample |
|---|---|---|
| `Send` | Ownership can pass to another branch | `Rc<T>` |
| `Sync` | `&T` can be shared across branches | `Cell<T>`, `RefCell<T>` |

The link between them: `T: Sync` means `&T: Send`. Sharing is sending a reference.

An empty function is enough to try which a type is:

```rust
use std::cell::Cell;
use std::sync::{Arc, Mutex};

fn assert_send<T: Send>() {}
fn assert_sync<T: Sync>() {}

fn main() {
    assert_send::<i32>();
    assert_send::<String>();
    assert_send::<Cell<i32>>();
    assert_sync::<Arc<i32>>();
    assert_sync::<Mutex<Cell<i32>>>();
    println!("all passed");
}
```

```text
all passed
```

If the program ran, all these types satisfy the condition. For `Rc` it does not compile:

```rust
use std::rc::Rc;

fn assert_send<T: Send>() {}

fn main() {
    assert_send::<Rc<i32>>();
}
```

```text
error[E0277]: `Rc<i32>` cannot be sent between threads safely
 --> main.rs:6:19
  |
6 |     assert_send::<Rc<i32>>();
  |                   ^^^^^^^ `Rc<i32>` cannot be sent between threads safely
  |
  = help: the trait `Send` is not implemented for `Rc<i32>`
note: required by a bound in `assert_send`
 --> main.rs:3:19
  |
3 | fn assert_send<T: Send>() {}
  |                   ^^^^ required by this bound in `assert_send`
```

## It comes by itself

If all fields of a struct are `Send`, the struct is `Send`. So these are called **auto traits**. For ordinary types you never think of them. A few types break the chain:

| Type | `Send` | `Sync` | Why |
|---|---|---|---|
| `i32`, `String`, `Vec<T>` | Yes | Yes | Ordinary ownership |
| `Rc<T>` | No | No | The counter is not atomic |
| `Cell<T>`, `RefCell<T>` | Yes | No | Writes through `&` without a lock |
| `Arc<T>` | `T: Send + Sync` | `T: Send + Sync` | An atomic counter, its contents are shared |
| `Mutex<T>` | `T: Send` | `T: Send` | A lock orders the access |
| `*const T`, `*mut T`, `NonNull<T>` | No | No | The compiler does not know what is behind |
| `MutexGuard<T>` | No | `T: Sync` | The lock must open on the same branch |

`Mutex<T>`'s condition stands out: it does not want `T: Sync`, because the lock gives one access at a time; even a value containing `RefCell` can be shared inside a `Mutex`. But it wants `T: Send`, because the value travels between branches.

## In your own type

A type holding a raw pointer is not `Send` by itself. `MyVec` from the earlier section does not pass to a branch:

```rust
fn main() {
    let list = MyVec::from_one(5);
    let handle = thread::spawn(move || println!("{}", list.first()));
    handle.join().unwrap();
}
```

```text
error[E0277]: `NonNull<i32>` cannot be sent between threads safely
  --> main.rs:30:32
   |
30 |     let handle = thread::spawn(move || println!("{}", list.first()));
   |                  ------------- -------^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   |                  |             |
   |                  |             `NonNull<i32>` cannot be sent between threads safely
   |                  |             within this `{closure@main.rs:30:32: 30:39}`
   |                  required by a bound introduced by this call
   |
   = help: within `{closure@main.rs:30:32: 30:39}`, the trait `Send` is not implemented
     for `NonNull<i32>`
note: required because it appears within the type `MyVec<i32>`
  --> main.rs:4:8
   |
 4 | struct MyVec<T> {
   |        ^^^^^
note: required because it's used within this closure
  --> main.rs:30:32
   |
30 |     let handle = thread::spawn(move || println!("{}", list.first()));
   |                                ^^^^^^^
note: required by a bound in `spawn`
```

This restriction is too strict: `MyVec` owns its items, just like `Vec`. Making the promise is up to us:

```rust
// SAFETY: MyVec owns its items, like Vec.
unsafe impl<T: Send> Send for MyVec<T> {}
// SAFETY: &MyVec gives only &T.
unsafe impl<T: Sync> Sync for MyVec<T> {}

fn main() {
    let list = MyVec::from_one(5);
    let handle = thread::spawn(move || println!("{} {}", list.first(), list.len));
    handle.join().unwrap();
}
```

```text
5 1
```

`unsafe impl` says: "the compiler cannot prove this promise, and I guarantee it." Writing the condition right is required: without `T: Send`, `MyVec<Rc<i32>>` would also pass to a branch, and the counter would race.

## A wrong promise

The compiler does not catch a wrong `unsafe impl`:

```rust
struct MyRc(Rc<i32>);

// WRONG: the counter inside is not atomic.
unsafe impl Send for MyRc {}
```

This compiles. As two branches copy and drop, the counter breaks, and the value is deleted early or never. The result is a data race, that is, undefined behavior. The question before writing `unsafe impl Send`: **"Is all the changing state of this type either owned or safe for concurrency?"**

## The reverse: taking the promise back

If a type must not be `Send`, the promise is taken back with `PhantomData`:

```rust
use std::marker::PhantomData;

struct Local {
    value: i32,
    _not_send: PhantomData<*const ()>,
}

fn main() {
    let local = Local { value: 3, _not_send: PhantomData };
    println!("{} {}", local.value, size_of::<Local>());
}
```

```text
3 4
```

It is used in types whose operating system resource must close on the same branch. `PhantomData<*const ()>` takes no space, but because it is a raw pointer it drops `Send` and `Sync`.

## UnsafeCell: the type under everything

Changing a value through `&T` is normally undefined behavior. The only exception is `UnsafeCell<T>`. `Cell`, `RefCell`, `Mutex` and the atomics are all built on it:

```rust
use std::cell::UnsafeCell;

struct MyCell<T> {
    value: UnsafeCell<T>,
}

impl<T: Copy> MyCell<T> {
    fn new(value: T) -> Self {
        MyCell { value: UnsafeCell::new(value) }
    }

    fn get(&self) -> T {
        // SAFETY: MyCell is not Sync and gives no references, so no one else reads now.
        unsafe { *self.value.get() }
    }

    fn set(&self, value: T) {
        // SAFETY: as above.
        unsafe { *self.value.get() = value };
    }
}

fn main() {
    let cell = MyCell::new(1);
    let a = &cell;
    let b = &cell;
    a.set(2);
    b.set(b.get() + 1);
    println!("{}", cell.get());
}
```

```text
3
```

`UnsafeCell` is not `Sync`, so `MyCell` is not `Sync` by itself either: `set` cannot be called across branches. The right behavior came with no extra effort. In the locks section we make the same type shareable with `unsafe impl Sync`.

## Summary

- `Send`: ownership passes. `Sync`: `&T` is shared.
- It is computed from fields; a raw pointer cuts the chain.
- `unsafe impl<T: Send> Send for X<T> {}`: do not write it without the condition.
- A wrong `unsafe impl` compiles and produces a data race.
- `PhantomData<*const ()>` takes the promise back.
- `UnsafeCell` is the only legal way to write through `&`.
