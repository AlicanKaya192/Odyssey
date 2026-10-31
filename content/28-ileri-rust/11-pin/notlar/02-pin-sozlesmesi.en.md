## What does the promise cover?

Once a value that is not `Unpin` has been pinned:

| Rule | Meaning |
|---|---|
| It does not move | No `mem::swap`, `mem::replace`, or taking ownership and placing it elsewhere |
| Its memory stays valid | It is not overwritten or freed before being dropped |
| `Drop` runs | A pinned value does not vanish without being dropped |

The last row matters: forgetting a pinned value with `mem::forget` and handing its memory to someone else also breaks the promise. `pin!` and `Box::pin` ensure this on their own.

## Where does unsafe come in?

| Operation | Safe? | Why |
|---|---|---|
| `pin!(f)` | Yes | The original variable is unreachable |
| `Box::pin(f)` | Yes | The contents are on the heap, the box is the sole owner |
| `Pin::new(&mut t)` | Yes | Only for `Unpin` |
| `get_mut` | Yes | Only for `Unpin` |
| `get_unchecked_mut` | No | The compiler cannot see that you do not move |
| `Pin::new_unchecked` | No | The compiler cannot check the promise |

## The rules of pin projection

If you decide to pin a field:

| Rule | Why |
|---|---|
| Do not move that field out of `self` | The promise |
| Do not write `Unpin` by hand for the struct | Otherwise outside code moves it with `get_mut` |
| Do not move the field inside `Drop` | `drop` takes `&mut self`, and the compiler does not see |
| Do not reuse the memory without dropping | The promise |

None of these rules apply to fields you do not pin: you can take the value out with `Option::take`. `func` in the `Map` exercise is like that.

In short, one question per field: will I give this field with `Pin` or with a plain `&mut`? Doing both is a mistake.

## Why so complicated?

In other languages a garbage collector updates references while moving objects. In Rust a move is only a byte copy, with no runtime work at all. The price of this choice is a separate type contract for the rare self-referencing case. An everyday user writes `async fn` and `.await`, and the compiler handles this detail. You mostly meet `Pin` when writing your own `Future` by hand.

## Before writing it by hand

Often these are enough instead of a wrapper:

| Need | Easier way |
|---|---|
| Two jobs in order | Two `.await`s in an `async` block |
| Transforming a result | `async { f(g().await) }` |
| Pin projection in a real project | The `pin-project` crate |
| A future from a closure | `std::future::poll_fn` |
