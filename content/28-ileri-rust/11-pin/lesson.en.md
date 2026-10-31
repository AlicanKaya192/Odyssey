# Pin

For two sections we have written `self: Pin<&mut Self>`, used `pin!` and `Box::pin`, and said "we will see why later". Its turn has come. `Pin` is the solution to a single problem: values that reference themselves.

## A struct that breaks when moved

Moving a value in Rust means copying its bytes elsewhere. Most of the time that is no problem. But it is if one field of a struct shows another field of the same struct:

```rust
use std::{mem, ptr};

struct SelfRef {
    value: String,
    pointer: *const String,
}

impl SelfRef {
    fn new(text: &str) -> Self {
        SelfRef { value: text.to_string(), pointer: ptr::null() }
    }

    fn init(&mut self) {
        self.pointer = &self.value;
    }

    fn read(&self) -> &str {
        // SAFETY: a and b both stay alive until the end of main.
        unsafe { &*self.pointer }
    }
}

fn main() {
    let mut a = SelfRef::new("first");
    let mut b = SelfRef::new("second");
    a.init();
    b.init();
    println!("value {}, pointer reads {}", a.value, a.read());

    mem::swap(&mut a, &mut b);
    println!("value {}, pointer reads {}", a.value, a.read());
}
```

```text
value first, pointer reads first
value second, pointer reads first
```

`mem::swap` exchanged the bytes of the two structs. `value` is now `second`, but `pointer` still shows the old place and reads `first`. The struct became inconsistent with itself. Since both structs are alive here we only read a wrong value; had one been dropped, it would be undefined behaviour.

In ordinary Rust you cannot write this struct with references; the borrow checker does not allow it. We wrote it with a raw pointer.

## An async fn is such a struct too

Look at this innocent code:

```rust
async fn holds() -> u32 {
    let value = 5;
    let reference = &value;
    pause().await;
    *reference + 1
}

fn main() {
    println!("{}", block_on(holds()));
}
```

```text
6
```

We saw it in the last sections: variables crossing an `.await` are stored inside the state machine. Both `value` and `reference` sit inside the same future, so **`reference` shows a field of its own struct**. If the future moves while waiting at the `.await`, `reference` shows the old address.

So there were two options: forbid references crossing an `.await`, or guarantee that a future that has started being polled will not move. Rust chose the second.

Moving before the first poll is no problem, because the body has not run and there is no reference inside. That is why we can freely move the result of an `async fn` call. The promise is needed when polling starts.

## Pin: the promise not to move

`Pin<P>` is a type wrapping a pointer. It says one thing: **the value shown will not move from its place until dropped.**

It does nothing at runtime:

```rust
use std::pin::Pin;

fn main() {
    println!("{}", size_of::<Pin<&mut u64>>() == size_of::<&mut u64>());
    println!("{}", size_of::<Pin<Box<u64>>>() == size_of::<Box<u64>>());
}
```

```text
true
true
```

All the work is at the type level. Moving needs ownership of the value or a `&mut T` (`mem::swap` works this way). `Pin<&mut T>` does not give you that `&mut T`. You cannot move what you cannot reach.

Note: what stays fixed is **the value shown**, not the pointer itself. You can move a `Pin<Box<T>>` anywhere; the box moves, and the value inside stays in place.

## Unpin: "It does not matter for me"

Most types do not reference themselves; moving them is always safe. They do not need all this ceremony. `Unpin` is the trait that says so. Like `Send`, it is implemented automatically:

```rust
use std::marker::PhantomPinned;
use std::pin::Pin;

fn needs_unpin<T: Unpin>() {}

fn main() {
    needs_unpin::<i32>();
    needs_unpin::<String>();
    needs_unpin::<Vec<u8>>();
    needs_unpin::<Box<PhantomPinned>>();
    needs_unpin::<Pin<Box<PhantomPinned>>>();
    println!("all of them are Unpin");
}
```

```text
all of them are Unpin
```

`Box<PhantomPinned>` and `Pin<Box<...>>` are `Unpin` too, because only a pointer moves.

If a type is `Unpin`, `Pin` has no effect: you pin with `Pin::new` and get `&mut T` back with `get_mut`. That is why plain structs like `Countdown` gave us no trouble in the last sections.

An `async fn` future, however, is **not** `Unpin`:

```rust
use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Waker};

async fn pause() {}

async fn holds() -> u32 {
    let value = 5;
    let reference = &value;
    pause().await;
    *reference + 1
}

fn main() {
    let mut future = holds();
    let mut cx = Context::from_waker(Waker::noop());
    let _ = Pin::new(&mut future).poll(&mut cx);
}
```

```text
error[E0277]: `{async fn body of holds()}` cannot be unpinned
  --> main.rs:17:22
   |
 7 | async fn holds() -> u32 {
   |                     --- within this `impl Future<Output = u32>`
...
17 |     let _ = Pin::new(&mut future).poll(&mut cx);
   |             -------- ^^^^^^^^^^^ within `impl Future<Output = u32>`, the trait
   `Unpin` is not implemented for `{async fn body of holds()}`
   |             |
   |             required by a bound introduced by this call
   |
   = note: consider using the `pin!` macro
           consider using `Box::pin` if you need to access the pinned value outside of
           the current scope
note: required because it appears within the type `impl Future<Output = u32>`
  --> main.rs:7:21
   |
 7 | async fn holds() -> u32 {
   |                     ^^^
note: required by a bound in `Pin::<Ptr>::new`
```

The compiler stops the wrong use right here. This is also the answer to why `Join` required `Unpin` earlier and why we wrapped `async fn` futures with `Box::pin`.

## Two ways of pinning

```rust
async fn work(name: &str) -> String {
    pause().await;
    format!("{name} finished")
}

fn main() {
    let mut cx = Context::from_waker(Waker::noop());

    let mut on_stack = pin!(work("stack"));
    while on_stack.as_mut().poll(&mut cx).is_pending() {}

    let mut on_heap = Box::pin(work("heap"));
    let result = loop {
        if let Poll::Ready(text) = on_heap.as_mut().poll(&mut cx) {
            break text;
        }
    };
    println!("{result}");
}
```

```text
heap finished
```

| Way | Where it sits | When |
|---|---|---|
| `pin!(f)` | In its scope | If it finishes in the scope; no allocation |
| `Box::pin(f)` | On the heap | If it outlives the scope or must move (tasks) |

`pin!` moves the value into itself. The original variable can no longer be used, so there is no way left to break the promise.

## A safe self-referencing struct

Let us write the first struct correctly. `PhantomPinned` is a zero-sized field that removes `Unpin` from the struct:

```rust
use std::marker::PhantomPinned;
use std::pin::Pin;
use std::ptr;

struct SelfRef {
    value: String,
    pointer: *const String,
    _pin: PhantomPinned,
}

impl SelfRef {
    fn new(text: &str) -> Pin<Box<Self>> {
        let mut boxed = Box::pin(SelfRef {
            value: text.to_string(),
            pointer: ptr::null(),
            _pin: PhantomPinned,
        });
        let pointer: *const String = &boxed.value;
        // SAFETY: writing a field does not move the struct.
        unsafe { boxed.as_mut().get_unchecked_mut().pointer = pointer };
        boxed
    }

    fn read(self: Pin<&Self>) -> &str {
        // SAFETY: the struct is pinned, so the pointer still shows its field.
        unsafe { &*self.pointer }
    }
}

fn main() {
    let mut a = SelfRef::new("first");
    let mut b = SelfRef::new("second");
    std::mem::swap(&mut a, &mut b);
    println!("value {}, pointer reads {}", a.value, a.as_ref().read());
}
```

```text
value second, pointer reads second
```

The same `mem::swap`, but now it exchanges the boxes; the contents stayed in place, and the value and pointer agree. Since the struct is not `Unpin`, writing the `pointer` field needed `get_unchecked_mut`.

If we try to get the value with `&mut`:

```rust
use std::marker::PhantomPinned;

struct Stuck {
    value: u32,
    _pin: PhantomPinned,
}

fn main() {
    let mut boxed = Box::pin(Stuck { value: 1, _pin: PhantomPinned });
    let stuck: &mut Stuck = boxed.as_mut().get_mut();
    stuck.value = 2;
}
```

```text
error[E0277]: `PhantomPinned` cannot be unpinned
  --> main.rs:10:44
   |
10 |     let stuck: &mut Stuck = boxed.as_mut().get_mut();
   |                                            ^^^^^^^ within `Stuck`, the trait
   `Unpin` is not implemented for `PhantomPinned`
   |
   = note: consider using the `pin!` macro
           consider using `Box::pin` if you need to access the pinned value outside of
           the current scope
note: required because it appears within the type `Stuck`
  --> main.rs:3:8
   |
 3 | struct Stuck {
   |        ^^^^^
note: required by a bound in `Pin::<&'a mut T>::get_mut`
```

## Pin projection: polling an inner future

Here is the real practical matter: you are writing a future that wraps a future, and the inner future is not `Unpin`. You have `Pin<&mut Self>` and you need `Pin<&mut F>`. This is called **pin projection**:

```rust
struct Counted<F> {
    inner: F,
    polls: u32,
}

impl<F: Future> Future for Counted<F> {
    type Output = F::Output;

    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<F::Output> {
        // SAFETY: inner is never moved out of self.
        let this = unsafe { self.get_unchecked_mut() };
        this.polls += 1;
        // SAFETY: self is pinned, so its inner field stays in place too.
        let inner = unsafe { Pin::new_unchecked(&mut this.inner) };
        inner.poll(cx)
    }
}

async fn two_pauses() -> u32 {
    pause().await;
    pause().await;
    7
}

fn main() {
    let mut future = pin!(Counted { inner: two_pauses(), polls: 0 });
    let mut cx = Context::from_waker(Waker::noop());
    let value = loop {
        if let Poll::Ready(value) = future.as_mut().poll(&mut cx) {
            break value;
        }
    };
    println!("value {value}, polls {}", future.polls);
}
```

```text
value 7, polls 3
```

There are two `unsafe`s, and in both the promise is ours:

- `get_unchecked_mut`: "I will not move `self`."
- `Pin::new_unchecked`: "I will not move `inner` either; if `self` is pinned, so is its field."

`polls` was not pinned: we changed it with a plain `&mut`, because moving it does not matter. The decision is made per field:

| Field | Decision | Access |
|---|---|---|
| Inner future | Pinned | `Pin::new_unchecked(&mut this.inner)` |
| Counter, flag, result | Not pinned | `&mut this.field`, may be moved |

Now you can write `Join` without the `Unpin` condition and `Box::pin`; one of the exercises is exactly that. In a real project, instead of writing these `unsafe`s by hand, the `pin-project` crate is used, which generates the same with a macro.

## Summary

- Moving is copying bytes; a self-referencing struct breaks when moved.
- A reference crossing an `.await` makes the future a self-referencing struct.
- `Pin<P>`: the value shown will not move until dropped. No runtime cost.
- `Unpin`: types for which pinning does not matter; most types. Not an `async fn` future.
- `pin!` pins in the scope, `Box::pin` on the heap.
- Pin projection: an inner future with `Pin::new_unchecked`, ordinary fields with a plain `&mut`.

That completes the foundations of async: `Future`, the waker, the executor and `Pin`.
