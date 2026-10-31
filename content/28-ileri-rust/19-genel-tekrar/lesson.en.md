# Overall Review

This module took Rust from "using it" to "knowing what is underneath". This section teaches nothing new; it combines the pieces. The quiz and exercises are the same: each question is from another section.

## The module in one program

The program below uses most of the module. If you can explain every line, this module is done:

```rust
use std::alloc::{Layout, alloc, dealloc};
use std::future::Future;
use std::pin::{Pin, pin};
use std::ptr;
use std::sync::atomic::{AtomicU32, Ordering};
use std::task::{Context, Poll, Waker};

static POLLS: AtomicU32 = AtomicU32::new(0);

struct Pause(bool);

impl Future for Pause {
    type Output = ();

    fn poll(mut self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<()> {
        POLLS.fetch_add(1, Ordering::Relaxed);
        if self.0 {
            return Poll::Ready(());
        }
        self.0 = true;
        cx.waker().wake_by_ref();
        Poll::Pending
    }
}

struct RawBox {
    pointer: *mut u32,
}

impl RawBox {
    fn new(value: u32) -> Self {
        let layout = Layout::new::<u32>();
        // SAFETY: u32 has a non-zero size.
        let pointer = unsafe { alloc(layout) }.cast::<u32>();
        assert!(!pointer.is_null());
        // SAFETY: the pointer is valid and aligned for a u32.
        unsafe { ptr::write(pointer, value) };
        RawBox { pointer }
    }

    fn get(&self) -> u32 {
        // SAFETY: new wrote a value, and drop has not run.
        unsafe { *self.pointer }
    }
}

impl Drop for RawBox {
    fn drop(&mut self) {
        // SAFETY: the pointer came from alloc with the same layout.
        unsafe { dealloc(self.pointer.cast(), Layout::new::<u32>()) };
    }
}

macro_rules! total {
    ($($x:expr),* $(,)?) => { 0 $(+ $x)* };
}

async fn work() -> u32 {
    let held = RawBox::new(40);
    Pause(false).await;
    total!(held.get(), 1, 1)
}

fn main() {
    let mut future = pin!(work());
    let mut cx = Context::from_waker(Waker::noop());
    let value = loop {
        if let Poll::Ready(value) = future.as_mut().poll(&mut cx) {
            break value;
        }
    };
    println!("{value} after {} polls", POLLS.load(Ordering::Relaxed));
}
```

```text
42 after 2 polls
```

| Place | Topic |
|---|---|
| `alloc`, `dealloc`, `ptr::write` | Your own memory management, `Layout` |
| `// SAFETY:` | The reason for `unsafe` |
| `Drop for RawBox` | Moving ownership to a raw pointer |
| `AtomicU32`, `Ordering::Relaxed` | Atomics |
| `impl Future for Pause` | A future by hand, `Poll`, a waker |
| `async fn work` | A state machine; `held` crosses the `.await` and sits in the future |
| `pin!`, `Waker::noop` | Pinning, the smallest executor |
| `macro_rules! total` | A repetition pattern |

## The four most important ideas

**1. `unsafe` is making a promise.** It does not turn checks off; it asks you to take on what the compiler cannot prove. The caller must be aware of that promise too:

```rust
unsafe fn read(pointer: *const u32) -> u32 {
    unsafe { *pointer }
}

fn main() {
    let value = 1;
    println!("{}", read(&value));
}
```

```text
error[E0133]: call to unsafe function `read` is unsafe and requires unsafe block
 --> main.rs:7:20
  |
7 |     println!("{}", read(&value));
  |                    ^^^^^^^^^^^^ call to unsafe function
  |
  = note: consult the function's documentation for information on how to avoid undefined
    behavior
```

The best `unsafe` is shut into a small place and opened to the outside through a safe interface. Better still is writing the promise into a type, like `Producer` in the capstone project.

**2. `Send` and `Sync` make branches safe through types.** A data race is not a runtime surprise but a compile error:

```rust
use std::cell::Cell;
use std::thread;

fn main() {
    let shared = Cell::new(1);
    thread::scope(|s| {
        s.spawn(|| shared.set(2));
    });
}
```

```text
error[E0277]: `Cell<i32>` cannot be shared between threads safely
 --> main.rs:7:17
  |
7 |         s.spawn(|| shared.set(2));
  |           ----- ^^^^^^^^^^^^^^^^ `Cell<i32>` cannot be shared between threads safely
  |           |
  |           required by a bound introduced by this call
  |
  = help: the trait `Sync` is not implemented for `Cell<i32>`
  = note: if you want to do aliasing and mutation between multiple threads, use
    `std::sync::RwLock` or `std::sync::atomic::AtomicI32` instead
  = note: required for `&Cell<i32>` to implement `Send`
note: required because it's used within this closure
 --> main.rs:7:17
  |
7 |         s.spawn(|| shared.set(2));
  |                 ^^
note: required by a bound in `Scope::<'scope, 'env>::spawn`
```

**3. A future is a state machine.** It does not run by itself; it is polled. `.await` does not wait; it passes `Pending` upward. A future that does not tell silently hangs.

**4. Moving is copying bytes, which is why `Pin` exists.** A self-referencing value breaks when moved. An `async fn` is such a value, and the compiler stops the wrong use:

```rust
use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Waker};

async fn work() {}

fn main() {
    let mut future = work();
    let mut cx = Context::from_waker(Waker::noop());
    let _ = Pin::new(&mut future).poll(&mut cx);
}
```

```text
error[E0277]: `{async fn body of work()}` cannot be unpinned
  --> main.rs:10:22
   |
 5 | async fn work() {}
   |                - within this `impl Future<Output = ()>`
...
10 |     let _ = Pin::new(&mut future).poll(&mut cx);
   |             -------- ^^^^^^^^^^^ within `impl Future<Output = ()>`, the trait
   `Unpin` is not implemented for `{async fn body of work()}`
   |             |
   |             required by a bound introduced by this call
   |
   = note: consider using the `pin!` macro
           consider using `Box::pin` if you need to access the pinned value outside of
           the current scope
note: required because it appears within the type `impl Future<Output = ()>`
  --> main.rs:5:16
   |
 5 | async fn work() {}
   |                ^
note: required by a bound in `Pin::<Ptr>::new`
```

## A short summary

| Section | One sentence |
|---|---|
| `unsafe`, raw pointers | Five extra powers; checks continue |
| Memory layout, `MaybeUninit` | Size, alignment, unbuilt memory |
| Your own `Vec` | `alloc`, `realloc`, `Drop` together |
| `PhantomData`, variance | How lifetimes relate to types |
| `Send`, `Sync`, atomics | Branch safety and memory order |
| Spinlock, lock-free structures | Hard work that looks easy |
| `Future`, executors | Polling, wakers, a task queue |
| `Pin` | The promise not to move |
| Macros | Producing code at compile time |
| FFI | Talking to C, ownership at the boundary |
| `no_std` | The `core`, `alloc`, `std` layers |
| Performance | Measure first |

If a topic gives you trouble, the links at the end of the quiz take you to that section.
