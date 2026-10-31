## Tools

| Name | What it does | Condition |
|---|---|---|
| `Pin::new(&mut t)` | Pins | `T: Unpin` |
| `pin!(f)` | Pins in the scope | None |
| `Box::pin(f)` | Pins on the heap | None |
| `pinned.as_mut()` | Reborrows `Pin<&mut T>` | None |
| `pinned.as_ref()` | Gives `Pin<&T>` | None |
| `pinned.get_mut()` | Gives `&mut T` | `T: Unpin` |
| `pinned.get_unchecked_mut()` | Gives `&mut T` | `unsafe` |
| `Pin::new_unchecked(p)` | Pins | `unsafe` |

## Which type is Unpin?

| Type | `Unpin`? |
|---|---|
| `i32`, `String`, `Vec<T>` | Yes |
| A struct with only `Unpin` fields | Yes |
| `Box<T>` | Yes, whatever `T` is |
| `Pin<Box<T>>` | Yes, whatever `T` is |
| An `async fn` or `async` block future | No |
| A struct with a `PhantomPinned` field | No |

## Decision table

| Situation | Do |
|---|---|
| Writing `Future` for a plain struct | `mut self: Pin<&mut Self>`, `self.field` |
| Inner futures are `Unpin` | `self.get_mut()`, `Pin::new(&mut this.inner)` |
| An inner future is not `Unpin` | Pin projection |
| Polling an `async fn` in place | `pin!` |
| Storing and moving a future | `Box::pin` |
| Keeping different futures together | `Pin<Box<dyn Future<...>>>` |

## A common mistake

The same `Pin<&mut F>` cannot be used twice, because `poll` consumes it:

```rust
use std::future::Future;
use std::pin::pin;
use std::task::{Context, Waker};

async fn pause() {}

fn main() {
    let future = pin!(pause());
    let mut cx = Context::from_waker(Waker::noop());
    let _ = future.poll(&mut cx);
    let _ = future.poll(&mut cx);
}
```

```text
error[E0382]: use of moved value: `future`
  --> main.rs:11:13
   |
 8 |     let future = pin!(pause());
   |         ------ move occurs because `future` has type `Pin<&mut impl Future<Output =
   ()>>`, which does not implement the `Copy` trait
 9 |     let mut cx = Context::from_waker(Waker::noop());
10 |     let _ = future.poll(&mut cx);
   |                    ------------- `future` moved due to this method call
11 |     let _ = future.poll(&mut cx);
   |             ^^^^^^ value used here after move
   |
note: `std::future::Future::poll` takes ownership of the receiver `self`, which moves
`future`
help: consider reborrowing the `Pin` instead of moving it
   |
10 |     let _ = future.as_mut().poll(&mut cx);
   |                   +++++++++
```

The fix: `future.as_mut().poll(&mut cx)` on each poll, with `let mut future`.
