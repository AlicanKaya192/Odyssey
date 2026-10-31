# Writing a Future by Hand

So far we opened branches to do several things at once. But if a server is waiting on ten thousand connections, most of that work is just **waiting**: for something to arrive from the network. Giving each wait its own branch is expensive. Rust's answer is `async`, and underneath it there is a single trait: `Future`.

In this section we remove the magic. We will write a `Future` by hand, poll it by hand, then see what an `async fn` really produces.

## Future: work that gets polled

A **future** is work that may not be finished yet. It does not run by itself; someone asks it "can you make progress?". That question is called a **poll**.

```rust
pub trait Future {
    type Output;

    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output>;
}

pub enum Poll<T> {
    Ready(T),
    Pending,
}
```

There are three parts:

- `Output`: the type of the value given when the work finishes.
- `Poll<T>`: the answer to a poll. `Ready(value)` means finished, `Pending` means not yet.
- `poll`: the method that asks the question.

`Pin<&mut Self>` looks frightening at first. For now read it as "a `&mut self` that promises not to move"; section 11 shows why. In the plain structs we write, we can reach fields like `self.left` directly.

`cx` (Context) carries a **waker**. A waker is the way to say "this future is worth polling again".

## Our first future

A countdown that says "not yet" twice and then finishes:

```rust
use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Poll, Waker};

struct Countdown {
    left: u32,
}

impl Future for Countdown {
    type Output = &'static str;

    fn poll(mut self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output> {
        if self.left == 0 {
            return Poll::Ready("done");
        }
        self.left -= 1;
        cx.waker().wake_by_ref();
        Poll::Pending
    }
}

fn main() {
    let mut future = Countdown { left: 2 };
    let mut cx = Context::from_waker(Waker::noop());
    let mut pinned = Pin::new(&mut future);
    println!("{:?}", pinned.as_mut().poll(&mut cx));
    println!("{:?}", pinned.as_mut().poll(&mut cx));
    println!("{:?}", pinned.as_mut().poll(&mut cx));
}
```

```text
Pending
Pending
Ready("done")
```

We polled three times and got three answers. The work advanced only when we asked; nothing runs in the background.

`Waker::noop()` is a ready-made waker that does nothing when told. It is handy for trying things by hand. `cx.waker().wake_by_ref()` means "poll me again". Nobody is listening here, but the contract requires it: a future returning `Pending` must make sure it will be polled again. We will measure why this matters in section 10.

## block_on: the smallest executor

The part of a program that polls futures is called an **executor**. Rust has none built into the language; you write one or take one as a crate. The smallest one is this: poll until it finishes.

```rust
fn block_on<F: Future>(future: F) -> F::Output {
    let mut future = pin!(future);
    let mut cx = Context::from_waker(Waker::noop());
    loop {
        if let Poll::Ready(value) = future.as_mut().poll(&mut cx) {
            return value;
        }
    }
}

fn main() {
    println!("{}", block_on(Countdown { left: 3 }));
}
```

```text
done
```

`pin!` fixes the future where it stands and gives the `Pin<&mut F>` needed to poll it. `F` can be any future; it does not have to be a plain struct.

This `block_on` spins: even after `Pending` it asks again at once. It tires the processor for nothing. A real executor sleeps and waits for the waker; we will write that in section 10.

## async fn: a function that produces a future

Writing `poll` by hand is tiring. `async fn` has the compiler do the same job. The first surprise is this:

```rust
async fn greet(name: &str) -> String {
    println!("greet runs");
    format!("hello {name}")
}

fn main() {
    let future = greet("ada");
    println!("future created");
    let text = block_on(future);
    println!("{text}");
}
```

```text
future created
greet runs
hello ada
```

The call `greet("ada")` did **not run** the body. It only returned a future. The body ran only when `block_on` polled it. Futures are lazy.

## What does .await do?

`.await` says "I stay here until this inner future finishes". But it does not stop the branch. Let us see what happens on each poll, line by line:

```rust
struct Step {
    name: &'static str,
    left: u32,
}

impl Future for Step {
    type Output = ();

    fn poll(mut self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<()> {
        println!("  {} left {}", self.name, self.left);
        if self.left == 0 {
            return Poll::Ready(());
        }
        self.left -= 1;
        cx.waker().wake_by_ref();
        Poll::Pending
    }
}

async fn work() -> u32 {
    println!("start");
    Step { name: "a", left: 1 }.await;
    println!("a finished");
    Step { name: "b", left: 1 }.await;
    println!("b finished");
    7
}

fn main() {
    let mut future = pin!(work());
    let mut cx = Context::from_waker(Waker::noop());
    let mut round = 1;
    loop {
        println!("poll {round}");
        if let Poll::Ready(value) = future.as_mut().poll(&mut cx) {
            println!("result {value}");
            break;
        }
        round += 1;
    }
}
```

```text
poll 1
start
  a left 1
poll 2
  a left 0
a finished
  b left 1
poll 3
  b left 0
b finished
result 7
```

Read the output carefully:

- `start` was written only once. The second poll did not restart; it continued from where it stopped.
- When `a` said `Pending`, `work` returned `Pending` too and went back to `main`. `.await` **does not wait, it returns**.
- When `a` finished, `work` continued inside the same poll and reached `b`.

How can a function continue from where it stopped? It cannot. The compiler turns it into something else.

## An async fn is really a state machine

Let us write what `work` does by hand. An `enum` holds the answer to "where am I?":

```rust
enum Work {
    Start,
    WaitA(Step),
    WaitB(Step),
    Done,
}

impl Future for Work {
    type Output = u32;

    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<u32> {
        let this = self.get_mut();
        loop {
            match this {
                Work::Start => {
                    println!("start");
                    *this = Work::WaitA(Step { name: "a", left: 1 });
                }
                Work::WaitA(step) => {
                    if Pin::new(step).poll(cx).is_pending() {
                        return Poll::Pending;
                    }
                    println!("a finished");
                    *this = Work::WaitB(Step { name: "b", left: 1 });
                }
                Work::WaitB(step) => {
                    if Pin::new(step).poll(cx).is_pending() {
                        return Poll::Pending;
                    }
                    println!("b finished");
                    *this = Work::Done;
                    return Poll::Ready(7);
                }
                Work::Done => panic!("polled after completion"),
            }
        }
    }
}

```

```text
poll 1
start
  a left 1
poll 2
  a left 0
a finished
  b left 1
poll 3
  b left 0
b finished
result 7
```

The output is exactly the same as the `async fn`. What the compiler produces is not exactly this, but the idea is the same: each `.await` is a state, and `poll` means "continue from the state you are in". No magic; it produces an `enum` we could write ourselves.

This `enum` also says something about size: every local variable that crosses an `.await` has to be stored inside the state.

```rust
async fn pause() {}

async fn keeps_buffer() {
    let buffer = [1u8; 1024];
    pause().await;
    println!("{}", buffer[0]);
}

async fn drops_buffer() {
    {
        let buffer = [1u8; 1024];
        println!("{}", buffer[0]);
    }
    pause().await;
}

fn main() {
    println!("keeps: {}", size_of_val(&keeps_buffer()) > 1024);
    println!("drops: {}", size_of_val(&drops_buffer()) > 1024);
}
```

```text
keeps: true
drops: false
```

In `keeps_buffer` the array is needed after the `.await` too, so it sits inside the future. In `drops_buffer` its scope ends before the `.await`, and the future does not grow. That is why not carrying big values across an `.await` is more than fussiness.

## Two jobs on one branch

Here is the real gain. Let us write `Join`, which advances two futures at once. `Yield` is a small future that says `Pending` once and gives up its turn:

```rust
struct Yield {
    done: bool,
}

impl Future for Yield {
    type Output = ();

    fn poll(mut self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<()> {
        if self.done {
            return Poll::Ready(());
        }
        self.done = true;
        cx.waker().wake_by_ref();
        Poll::Pending
    }
}

struct Join<A, B> {
    a: A,
    b: B,
    a_done: bool,
    b_done: bool,
}

impl<A, B> Future for Join<A, B>
where
    A: Future<Output = ()> + Unpin,
    B: Future<Output = ()> + Unpin,
{
    type Output = ();

    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<()> {
        let this = self.get_mut();
        if !this.a_done {
            this.a_done = Pin::new(&mut this.a).poll(cx).is_ready();
        }
        if !this.b_done {
            this.b_done = Pin::new(&mut this.b).poll(cx).is_ready();
        }
        if this.a_done && this.b_done {
            Poll::Ready(())
        } else {
            Poll::Pending
        }
    }
}

async fn worker(name: &str, rounds: u32) {
    for round in 0..rounds {
        println!("{name} {round}");
        Yield { done: false }.await;
    }
}

fn main() {
    let a = Box::pin(worker("a", 2));
    let b = Box::pin(worker("b", 2));
    block_on(Join { a, b, a_done: false, b_done: false });
}
```

```text
a 0
b 0
a 1
b 1
```

There is one branch, yet the jobs advanced in turn. This is called **concurrency**; it is not **parallelism**, because at no moment do two jobs run at once.

`Box::pin` puts the future of `worker` on the heap and fixes it there. That lets `Join` poll it easily with `Pin::new`. Section 11 shows why as well.

What if we remove `Yield`?

```rust
async fn worker(name: &str, rounds: u32) {
    for round in 0..rounds {
        println!("{name} {round}");
    }
}

```

```text
a 0
a 1
b 0
b 1
```

`a` never gave up its turn. This is the most important rule of `async`: the turn changes only at an `.await`, and only if the inner future says `Pending`. The executor cannot stop anyone by force; the jobs **cooperate**. That is why in `async` code a long calculation or `thread::sleep` stops the whole branch, meaning all the other futures.

## Why all this effort?

```rust
async fn worker(rounds: u32) -> u32 {
    for _ in 0..rounds {
        Yield { done: false }.await;
    }
    rounds
}

fn main() {
    let mut tasks: Vec<_> = (0..10_000).map(|_| Box::pin(worker(3))).collect();
    println!("one task under 1 KiB: {}", size_of_val(&*tasks[0]) < 1024);

    let mut cx = Context::from_waker(Waker::noop());
    let mut sum = 0;
    let mut rounds = 0;
    while !tasks.is_empty() {
        rounds += 1;
        tasks.retain_mut(|task| match task.as_mut().poll(&mut cx) {
            Poll::Ready(value) => {
                sum += value;
                false
            }
            Poll::Pending => true,
        });
    }
    println!("sum {sum}, rounds {rounds}");
}
```

```text
one task under 1 KiB: true
sum 30000, rounds 4
```

On one branch, ten thousand jobs finished in four rounds, each under 1 KiB. A new branch's stack in Rust, according to the documentation, is currently 2 MiB by default. That is the difference when much of the work is waiting. If the work calculates rather than waits there is no gain; branches are the right answer there.

## Summary

- A `Future` is work polled with `poll`: `Ready(value)` or `Pending`.
- A future does not run by itself; an executor polls it.
- Calling an `async fn` only produces a future; the body runs on the first poll.
- `.await` does not wait, it passes `Pending` upward; the next poll continues from where it stopped.
- An `async fn` is a state machine the compiler produces; variables crossing an `.await` live inside it.
- The turn changes only at `.await`. There is concurrency, not parallelism.

Next comes a real executor: one that does not spin, and wakes with the waker.
