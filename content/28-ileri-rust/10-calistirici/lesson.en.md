# Our Own Async Executor

In the last section `block_on` was spinning, and we said "a real executor sleeps". Now we write it: first a sleeping `block_on`, then a small executor that runs many jobs together.

## First, measure the problem

We need a future that really waits. `Timer` opens a branch in the background and counts the work as finished when the time is up. (We will read its code shortly.) A 50 millisecond wait with the spinning method:

```rust
fn spin_polls<F: Future>(future: F) -> u64 {
    let mut future = pin!(future);
    let mut cx = Context::from_waker(Waker::noop());
    let mut polls = 0;
    loop {
        polls += 1;
        if future.as_mut().poll(&mut cx).is_ready() {
            return polls;
        }
    }
}

fn main() {
    println!("over 1000 polls: {}", spin_polls(Timer::new(50)) > 1000);
}
```

```text
over 1000 polls: true
```

We asked thousands of times during a wait in which nothing happened. The processor ran at full load for nothing all that time. What we want: ask, sleep if the answer is `Pending`, and ask again when someone wakes us.

## Waker: the "ask again" message

In the last section we used `Waker::noop()`, and the message went nowhere. For the message to really do something, there is the `Wake` trait. We write a type, implement `Wake`, and convert it to a waker with `Waker::from`:

```rust
use std::future::Future;
use std::pin::pin;
use std::sync::Arc;
use std::task::{Context, Poll, Wake, Waker};
use std::thread::{self, Thread};

struct ThreadWaker(Thread);

impl Wake for ThreadWaker {
    fn wake(self: Arc<Self>) {
        self.0.unpark();
    }
}

fn block_on<F: Future>(future: F) -> F::Output {
    let mut future = pin!(future);
    let waker = Waker::from(Arc::new(ThreadWaker(thread::current())));
    let mut cx = Context::from_waker(&waker);
    loop {
        match future.as_mut().poll(&mut cx) {
            Poll::Ready(value) => return value,
            Poll::Pending => thread::park(),
        }
    }
}

fn main() {
    println!("{}", block_on(async { 40 + 2 }));
}
```

```text
42
```

Piece by piece:

- `ThreadWaker(Thread)`: holds the identity of the branch to wake. `thread::current()` gives the current branch.
- `wake(self: Arc<Self>)`: when the message comes, it wakes the branch with `unpark`. `Arc` is required, because a waker is copied and travels between branches.
- `thread::park()`: sleeps the branch until an `unpark`, freeing the processor.

Let us measure:

```rust
fn counted_block_on<F: Future>(future: F) -> u32 {
    let mut future = pin!(future);
    let waker = Waker::from(Arc::new(ThreadWaker(thread::current())));
    let mut cx = Context::from_waker(&waker);
    let mut polls = 0;
    loop {
        polls += 1;
        match future.as_mut().poll(&mut cx) {
            Poll::Ready(_) => return polls,
            Poll::Pending => thread::park(),
        }
    }
}

fn main() {
    println!("polls: {}", counted_block_on(Timer::new(50)));
}
```

```text
polls: 2
```

Two polls instead of thousands: one at the start, one when the message comes.

`park` can also return for no reason (its documentation says so). That is fine, because we are in a loop: we poll again, the future still says `Pending`, and we sleep again.

So if the message comes exactly between `poll` and `park`, is it lost? No. `unpark` leaves a token; the next `park` sees the token and returns at once:

```rust
use std::thread;

fn main() {
    thread::current().unpark();
    thread::park();
    println!("park returned at once");
}
```

```text
park returned at once
```

## The side giving the message: Timer

Storing the waker is the future's job. The one doing the real work (here the branch in the background) calls the stored waker when finished:

```rust
use std::future::Future;
use std::pin::{Pin, pin};
use std::sync::{Arc, Mutex};
use std::task::{Context, Poll, Wake, Waker};
use std::thread::{self, Thread};
use std::time::Duration;

struct Shared {
    done: bool,
    waker: Option<Waker>,
}

struct Timer {
    shared: Arc<Mutex<Shared>>,
}

impl Timer {
    fn new(ms: u64) -> Self {
        let shared = Arc::new(Mutex::new(Shared { done: false, waker: None }));
        let for_thread = shared.clone();
        thread::spawn(move || {
            thread::sleep(Duration::from_millis(ms));
            let waker = {
                let mut state = for_thread.lock().unwrap();
                state.done = true;
                state.waker.take()
            };
            if let Some(waker) = waker {
                waker.wake();
            }
        });
        Timer { shared }
    }
}

impl Future for Timer {
    type Output = ();

    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<()> {
        let mut state = self.shared.lock().unwrap();
        if state.done {
            return Poll::Ready(());
        }
        state.waker = Some(cx.waker().clone());
        Poll::Pending
    }
}

fn main() {
    block_on(Timer::new(20));
    println!("timer finished");
}
```

```text
timer finished
```

Three points to watch:

- `poll` stores the waker again **on each call**. The valid one is the latest poll's waker; the future may have moved to another task.
- Checking the state and storing the waker happen under the same lock. Otherwise the branch could write `done` and find a waker not stored yet, and the message would be lost.
- The branch takes the waker out of the lock and wakes it **after the lock is released**, so the woken work need not wait for the lock.

## If we break the contract

We promised this in the last section. This future finishes on the second poll but never tells anyone:

```rust
struct Forgetful {
    asked: bool,
}

impl Future for Forgetful {
    type Output = ();

    fn poll(mut self: Pin<&mut Self>, _cx: &mut Context<'_>) -> Poll<()> {
        if self.asked {
            return Poll::Ready(());
        }
        self.asked = true;
        Poll::Pending
    }
}

fn finishes_in<F: Future>(future: F, limit: Duration) -> bool {
    let mut future = pin!(future);
    let waker = Waker::from(Arc::new(ThreadWaker(thread::current())));
    let mut cx = Context::from_waker(&waker);
    let start = std::time::Instant::now();
    loop {
        if future.as_mut().poll(&mut cx).is_ready() {
            return true;
        }
        thread::park_timeout(limit);
        if start.elapsed() >= limit {
            return false;
        }
    }
}

fn spin<F: Future>(future: F) {
    let mut future = pin!(future);
    let mut cx = Context::from_waker(Waker::noop());
    while future.as_mut().poll(&mut cx).is_pending() {}
}

fn main() {
    spin(Forgetful { asked: false });
    println!("spinning: finished");
    let limit = Duration::from_millis(100);
    let finished = finishes_in(Forgetful { asked: false }, limit);
    println!("sleeping: finished = {finished}");
}
```

```text
spinning: finished
sleeping: finished = false
```

With the spinning method the mistake goes unseen, because it always asks. In the sleeping executor the future is never polled again. Here we set a time limit; in a real program it would silently hang forever. In async code, when you see "the program freezes but gives no error", this is the first place to look.

## Many jobs: task and queue

One `block_on` runs one future. Managing many jobs takes two concepts:

- **Task**: a top-level future the executor manages.
- **Queue**: the tasks ready to be polled.

The idea in one sentence: the executor takes a task from the queue and polls it, and `wake` puts the task back on the queue. A task that returned `Pending` is not on the queue, so it **uses no processor at all**.

```rust
use std::future::Future;
use std::pin::Pin;
use std::sync::mpsc::{Receiver, Sender, channel};
use std::sync::{Arc, Mutex};
use std::task::{Context, Poll, Wake, Waker};
use std::thread;
use std::time::{Duration, Instant};

type BoxFuture = Pin<Box<dyn Future<Output = ()> + Send>>;

struct Task {
    future: Mutex<Option<BoxFuture>>,
    queue: Sender<Arc<Task>>,
}

impl Wake for Task {
    fn wake(self: Arc<Self>) {
        let queue = self.queue.clone();
        let _ = queue.send(self);
    }
}

fn spawn<F>(queue: &Sender<Arc<Task>>, future: F)
where
    F: Future<Output = ()> + Send + 'static,
{
    let task = Task {
        future: Mutex::new(Some(Box::pin(future))),
        queue: queue.clone(),
    };
    queue.send(Arc::new(task)).unwrap();
}

fn run(queue: Receiver<Arc<Task>>) {
    while let Ok(task) = queue.recv() {
        let mut slot = task.future.lock().unwrap();
        if let Some(future) = slot.as_mut() {
            let waker = Waker::from(task.clone());
            let mut cx = Context::from_waker(&waker);
            if future.as_mut().poll(&mut cx).is_ready() {
                *slot = None;
            }
        }
    }
}

async fn worker(name: &'static str, ms: u64) {
    Timer::new(ms).await;
    println!("{name} finished");
}

fn main() {
    let (sender, receiver) = channel();
    let start = Instant::now();
    spawn(&sender, worker("a", 150));
    spawn(&sender, worker("b", 50));
    spawn(&sender, worker("c", 100));
    drop(sender);
    run(receiver);
    println!("under 300 ms: {}", start.elapsed() < Duration::from_millis(300));
}
```

```text
b finished
c finished
a finished
under 300 ms: true
```

What the parts do:

| Part | Its job |
|---|---|
| `Task` | The future and the way back to the queue |
| `Mutex<Option<...>>` | Using the future needs `&mut`; a finished future becomes `None` |
| `wake` | Puts the task on the queue |
| `spawn` | Builds the task and puts it on the queue the first time |
| `run` | Takes from the queue, polls |
| `drop(sender)` | When tasks finish the queue closes, `recv` errors, `run` ends |

The three timers total 300 milliseconds, but the work took less, because they waited together. The shortest finished first, and all of them printed on the single branch of `run`.

## The Send condition

`spawn` requires the future to be `Send`, because a waker may be called from another branch and real executors move tasks between branches. In the last section we saw that variables crossing an `.await` sit inside the future. The result:

```rust
use std::future::Future;
use std::rc::Rc;

async fn pause() {}

async fn counted() {
    let count = Rc::new(1);
    pause().await;
    println!("{count}");
}

fn spawn<F: Future + Send>(_future: F) {}

fn main() {
    spawn(counted());
}
```

```text
error: future cannot be sent between threads safely
  --> main.rs:15:11
   |
15 |     spawn(counted());
   |           ^^^^^^^^^ future returned by `counted` is not `Send`
   |
   = help: within `impl Future<Output = ()>`, the trait `Send` is not implemented for
     `Rc<i32>`
note: future is not `Send` as this value is used across an await
  --> main.rs:8:13
   |
 7 |     let count = Rc::new(1);
   |         ----- has type `Rc<i32>` which is not `Send`
 8 |     pause().await;
   |             ^^^^^ await occurs here, with `count` maybe used later
note: required by a bound in `spawn`
  --> main.rs:12:22
   |
12 | fn spawn<F: Future + Send>(_future: F) {}
   |                      ^^^^ required by this bound in `spawn`
```

The `Rc` crossed an `.await`, became part of the future, and the future stopped being `Send`. The solution: use `Arc`, or drop the `Rc` before the `.await`.

## Cancellation: dropping

Rust has no separate way to stop a future; **dropping** is enough. A dropped future is never polled again, and the `Drop` of the values inside runs:

```rust
struct Noisy;

impl Drop for Noisy {
    fn drop(&mut self) {
        println!("cleanup");
    }
}

async fn job() {
    let _guard = Noisy;
    println!("started");
    std::future::pending::<()>().await;
    println!("never printed");
}

fn main() {
    let mut future = Box::pin(job());
    let mut cx = Context::from_waker(Waker::noop());
    let _ = future.as_mut().poll(&mut cx);
    drop(future);
    println!("dropped");
}
```

```text
started
cleanup
dropped
```

`job` was waiting at an `.await`; the rest never ran, but `_guard` was cleaned up.

This idea is the basis of the **select** pattern: poll two futures together, take the first to finish, and drop the other. "Give up if this does not finish in 5 seconds" is written this way. It has a price too: a future can be cancelled at any `.await`, so work that must not stop halfway between two `.await`s has to be done in one piece.

## Summary

- A sleeping executor: `park` on `Pending`, `unpark` on the waker.
- The `Wake` trait builds a `Waker` from a type in an `Arc`.
- A future stores the waker on each poll; the side doing the work calls it when finished.
- A future that does not tell silently hangs in a sleeping executor.
- Task + queue = executor. `wake` puts the task on the queue, and a waiting task uses no processor.
- Because of `spawn`'s `Send` condition, an `Rc` crossing an `.await` does not compile.
- Cancelling is dropping; `Drop` runs.

Next is the question we put off for two sections: why does `Pin` exist?
