## The parts

| Name | What it does |
|---|---|
| `Future` | Work polled with `poll` |
| `Future::Output` | The type of the value given at the end |
| `Poll::Ready(v)` | Finished, the value is `v` |
| `Poll::Pending` | Not yet |
| `Context` | Goes along with the poll, carries the waker |
| `cx.waker()` | The current waker |
| `wake_by_ref()` | "Poll me again" |
| `Waker::noop()` | A waker that does nothing when told |
| `pin!(f)` | Fixes a future in place |
| `Box::pin(f)` | Fixes a future on the heap |

## The hand-written future pattern

| Step | Code |
|---|---|
| Finished? | `return Poll::Ready(value);` |
| Not finished | Advance the state |
| Tell | `cx.waker().wake_by_ref();` |
| Return | `Poll::Pending` |

In an `Unpin` struct, fields are reached as `self.field`; to borrow the field itself, use `self.get_mut()`. To poll an inner future, `Pin::new(&mut this.inner).poll(cx)`. Plain structs are `Unpin` on their own.

## async forms

| Form | Meaning |
|---|---|
| `async fn f() -> T` | When called, returns a future with `Output = T` |
| `async { ... }` | Produces a future in place, borrowing its surroundings |
| `async move { ... }` | Moves its surroundings into the future |
| `f().await` | Does not continue until finished, passing `Pending` meanwhile |

## Ready-made in the standard library

| Name | Behaviour |
|---|---|
| `std::future::ready(v)` | `Ready(v)` on the first poll |
| `std::future::pending()` | Never finishes |
| `std::future::poll_fn(f)` | Makes a future from a closure |

## Branch or async?

| Work | Right tool |
|---|---|
| Mostly waiting (network, disk) | `async` |
| Mostly calculating | A branch |
| A few waiting jobs | A branch is simpler |
| Tens of thousands of connections | `async` |
