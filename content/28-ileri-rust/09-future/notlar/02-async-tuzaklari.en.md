## Forgetting .await

Futures are lazy; call one and leave it, and nothing happens. Luckily the compiler warns:

```rust
async fn save() {}

fn main() {
    save();
}
```

```text
warning: unused implementer of `Future` that must be used
 --> main.rs:4:5
  |
4 |     save();
  |     ^^^^^^
  |
  = note: futures do nothing unless you `.await` or poll them
  = note: `#[warn(unused_must_use)]` (part of `#[warn(unused)]`) on by default
```

## .await outside async

Without an outer future to poll it, `.await` cannot be written:

```rust
fn main() {
    let value = std::future::ready(1).await;
    println!("{value}");
}
```

```text
error[E0728]: `await` is only allowed inside `async` functions and blocks
 --> main.rs:2:39
  |
1 | fn main() {
  | --------- this is not `async`
2 |     let value = std::future::ready(1).await;
  |                                       ^^^^^ only allowed inside `async` functions
  and blocks
```

Making `main` `async` does not solve it either, because nobody would poll it. The solution is an executor: `block_on(future)`.

## An async fn calling itself

If the state machine contained itself, its size would be infinite:

```rust
async fn count_down(n: u32) {
    if n > 0 {
        count_down(n - 1).await;
    }
}

fn main() {
    let _ = count_down(2);
}
```

```text
error[E0733]: recursion in an async fn requires boxing
 --> main.rs:1:1
  |
1 | async fn count_down(n: u32) {
  | ^^^^^^^^^^^^^^^^^^^^^^^^^^^
2 |     if n > 0 {
3 |         count_down(n - 1).await;
  |         ----------------------- recursive call here
  |
  = note: a recursive `async fn` call must introduce indirection such as `Box::pin` to
    avoid an infinitely sized future
```

The solution is to put the inner call on the heap. Only a pointer stays inside the structure now:

```rust
async fn count_down(n: u32) {
    if n > 0 {
        println!("{n}");
        Box::pin(count_down(n - 1)).await;
    }
}

fn main() {
    block_on(count_down(2));
}
```

```text
2
1
```

## Polling a finished future again

A future that returned `Ready` is done. Polling it again breaks the contract, and an `async fn` future panics:

```rust
async fn one() -> u32 {
    1
}

fn main() {
    let mut future = pin!(one());
    let mut cx = Context::from_waker(Waker::noop());
    println!("{:?}", future.as_mut().poll(&mut cx));
    println!("{:?}", future.as_mut().poll(&mut cx));
}
```

```text
Ready(1)

thread 'main' panicked at main.rs:4:23:
`async fn` resumed after completion
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

That is why a hand-written `Join` must not poll a finished future again.

## Blocking the branch

Inside an `async` body, `thread::sleep`, a long calculation or a blocking file read stops the whole branch. That is what happened in the lesson's example without `Yield`: the turn never changed. The rule is simple: no `.await`, no turn.

## Returning Pending without telling

Returning `Pending` without calling `cx.waker().wake_by_ref()` goes unnoticed in our spinning `block_on`, because it always asks again. In a real executor that sleeps, the future is never polled again and the program silently hangs. We will see this in section 10.
