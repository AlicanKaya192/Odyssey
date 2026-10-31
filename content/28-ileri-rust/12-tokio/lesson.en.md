# tokio

In the last three sections we saw `Future`, the waker, our own executor and `Pin`. The Rust language only defines `Future`;
the runtime that drives it is a package. In most real programs that package is **tokio**: worker threads, a timer, networking,
channels. It is the sturdy form of what we wrote by hand in our own executor.

In Odyssey its source comes with the program. In your own project you write `cargo add tokio --features full`. The first build
is slow because it builds tokio too (about 10 seconds on this computer); after that it takes under a second.

## A first program

```rust
#[tokio::main]
async fn main() {
    println!("hello from tokio");
}
```

```text
hello from tokio
```

`#[tokio::main]` is an attribute macro. `main` cannot be async, because nothing would drive it. The macro builds the runtime
and runs the body with `block_on`, so roughly it writes this:

```rust
fn main() {
    let runtime = tokio::runtime::Builder::new_multi_thread()
        .enable_all()
        .build()
        .unwrap();
    runtime.block_on(async {
        println!("inside the runtime");
    });
}
```

```text
inside the runtime
```

We wrote `block_on` ourselves. The difference here is that there are several worker threads underneath, and an idle worker takes
work from another's queue (work stealing).

## Together, not one after another

`.await` does not bring concurrency by itself: with two `.await`s in a row, the second starts when the first ends. To run them
together you write `join!`:

```rust
use std::time::{Duration, Instant};
use tokio::time::sleep;

async fn work(name: &str) -> String {
    sleep(Duration::from_millis(200)).await;
    format!("{name} done")
}

#[tokio::main]
async fn main() {
    let start = Instant::now();
    let a = work("a").await;
    let b = work("b").await;
    println!("{a}, {b}");
    println!("at least 400 ms: {}", start.elapsed().as_millis() >= 400);

    let start = Instant::now();
    let (a, b) = tokio::join!(work("a"), work("b"));
    println!("{a}, {b}");
    println!("under 400 ms: {}", start.elapsed().as_millis() < 400);
}
```

```text
a done, b done
at least 400 ms: true
a done, b done
under 400 ms: true
```

We printed a comparison instead of the time because the time changes on each run. `join!` polls the two futures in turn **in
the same task**; while one waits, the other makes progress.

## Starting a task: spawn

`tokio::spawn` starts a new **task**. A task is an independent unit of work driven by the runtime; it is much cheaper than a
thread and can run on another worker. That is why the future must be `Send` and `'static`; `async move` takes the data it needs
inside.

```rust
use std::time::Duration;
use tokio::time::sleep;

#[tokio::main]
async fn main() {
    let mut handles = Vec::new();
    for id in 0..3u64 {
        handles.push(tokio::spawn(async move {
            sleep(Duration::from_millis(100 - id * 30)).await;
            println!("finished {id}");
            id * 10
        }));
    }
    for handle in handles {
        println!("result {}", handle.await.unwrap());
    }
}
```

```text
finished 2
finished 1
finished 0
result 0
result 10
result 20
```

The tasks ended in the order 2, 1, 0, but we got the results in our `await` order. A task starts running as soon as it is
spawned; waiting on the `JoinHandle` is only for getting the result.

When a task panics the program does not stop; the error comes back through the `JoinHandle`:

```rust
#[tokio::main]
async fn main() {
    std::panic::set_hook(Box::new(|_| {}));
    let handle = tokio::spawn(async {
        let zero = "".len();
        10 / zero
    });
    let result = handle.await;
    println!("{}", result.is_err());
    println!("{}", result.unwrap_err().is_panic());
    println!("the program goes on");
}
```

```text
true
true
the program goes on
```

The `set_hook` here only silences the panic message, to keep the output clean.

## A race: select and timeout

`select!` waits on several futures at once, runs the **first to finish** and drops the others. `timeout` is the same idea ready
made:

```rust
use std::time::Duration;
use tokio::time::{sleep, timeout};

#[tokio::main]
async fn main() {
    tokio::select! {
        _ = sleep(Duration::from_millis(500)) => println!("slow won"),
        _ = sleep(Duration::from_millis(20)) => println!("fast won"),
    }

    let result = timeout(Duration::from_millis(20), sleep(Duration::from_secs(5))).await;
    println!("{result:?}");
    let result = timeout(Duration::from_millis(500), async { 42 }).await;
    println!("{result:?}");
}
```

```text
fast won
Err(Elapsed(()))
Ok(42)
```

**Cancellation** becomes visible here. In Rust, cancelling a future means dropping it: what follows the last `await` point never
runs. To stop a task from outside, `abort`:

```rust
use std::time::Duration;
use tokio::time::sleep;

#[tokio::main]
async fn main() {
    let handle = tokio::spawn(async {
        sleep(Duration::from_secs(60)).await;
        println!("never printed");
    });
    sleep(Duration::from_millis(10)).await;
    handle.abort();
    println!("{}", handle.await.unwrap_err().is_cancelled());
}
```

```text
true
```

## Channels

The cleanest way to share data between tasks is to send messages. `mpsc` is a channel with many senders and one receiver. The `8`
is the capacity: when the channel is full, `send` waits. This **backpressure** stops a fast producer from filling the memory.

```rust
use tokio::sync::mpsc;

#[tokio::main]
async fn main() {
    let (sender, mut receiver) = mpsc::channel(8);
    for id in 0..3 {
        let sender = sender.clone();
        tokio::spawn(async move {
            sender.send(id * 10).await.unwrap();
        });
    }
    drop(sender);

    let mut got = Vec::new();
    while let Some(value) = receiver.recv().await {
        got.push(value);
    }
    got.sort();
    println!("{got:?}");
}
```

```text
[0, 10, 20]
```

`drop(sender)` matters: `recv` does not give `None` until all senders are dropped. If we do not drop our own copy, the loop waits
forever.

Having one task manage a state and answer requests is a very common pattern. For the answer, a `oneshot`, a one-message channel,
goes inside the request:

```rust
use tokio::sync::{mpsc, oneshot};

enum Request {
    Add(i32),
    Total(oneshot::Sender<i32>),
}

#[tokio::main]
async fn main() {
    let (sender, mut receiver) = mpsc::channel(8);
    tokio::spawn(async move {
        let mut total = 0;
        while let Some(request) = receiver.recv().await {
            match request {
                Request::Add(n) => total += n,
                Request::Total(reply) => reply.send(total).unwrap(),
            }
        }
    });

    sender.send(Request::Add(5)).await.unwrap();
    sender.send(Request::Add(7)).await.unwrap();
    let (reply, answer) = oneshot::channel();
    sender.send(Request::Total(reply)).await.unwrap();
    println!("{}", answer.await.unwrap());
}
```

```text
12
```

Since `total` is in the hands of a single task, no lock is needed.

## Shared state

For a short job the standard `Mutex` is still the right choice, and it is faster:

```rust
use std::sync::{Arc, Mutex};

#[tokio::main]
async fn main() {
    let count = Arc::new(Mutex::new(0));
    let mut handles = Vec::new();
    for _ in 0..4 {
        let count = Arc::clone(&count);
        handles.push(tokio::spawn(async move {
            *count.lock().unwrap() += 1;
            tokio::task::yield_now().await;
        }));
    }
    for handle in handles {
        handle.await.unwrap();
    }
    println!("{}", count.lock().unwrap());
}
```

```text
4
```

There is one condition: the lock is not held across an `.await`. If you hold it the compiler stops you, because a `MutexGuard`
cannot move to another thread:

```rust
use std::sync::{Arc, Mutex};

#[tokio::main]
async fn main() {
    let count = Arc::new(Mutex::new(0));
    let handle = tokio::spawn(async move {
        let mut guard = count.lock().unwrap();
        tokio::task::yield_now().await;
        *guard += 1;
    });
    handle.await.unwrap();
}
```

```text
error: future cannot be sent between threads safely
   --> src/main.rs:6:18
    |
  6 |       let handle = tokio::spawn(async move {
    |  __________________^
  7 | |         let mut guard = count.lock().unwrap();
  8 | |         tokio::task::yield_now().await;
  9 | |         *guard += 1;
 10 | |     });
    | |______^ future created by async block is not `Send`
    |
    = help: within `{async block@src\main.rs:6:31: 6:41}`, the trait `Send` is not
      implemented for `std::sync::MutexGuard<'_, i32>`
note: future is not `Send` as this value is used across an await
   --> src/main.rs:8:34
    |
  7 |         let mut guard = count.lock().unwrap();
    |             --------- has type `std::sync::MutexGuard<'_, i32>` which is not
    `Send`
  8 |         tokio::task::yield_now().await;
    |                                  ^^^^^ await occurs here, with `mut guard` maybe
    used later
note: required by a bound in `tokio::spawn`
   --> rust-vendor/tokio/src/task/spawn.rs:176:21
    |
174 |     pub fn spawn<F>(future: F) -> JoinHandle<F::Output>
    |            ----- required by a bound in this function
175 |     where
176 |         F: Future + Send + 'static,
    |                     ^^^^ required by this bound in `spawn`
```

| Need | Use |
|---|---|
| A short job, no await | `std::sync::Mutex` |
| The lock is held across an await | `tokio::sync::Mutex` |
| One task manages the state | A channel |

To limit how many jobs run at once, a `Semaphore`:

```rust
use std::sync::Arc;
use std::sync::atomic::{AtomicUsize, Ordering};
use std::time::Duration;
use tokio::sync::Semaphore;
use tokio::time::sleep;

#[tokio::main]
async fn main() {
    let permits = Arc::new(Semaphore::new(3));
    let running = Arc::new(AtomicUsize::new(0));
    let highest = Arc::new(AtomicUsize::new(0));
    let mut handles = Vec::new();
    for _ in 0..10 {
        let permits = permits.clone();
        let running = running.clone();
        let highest = highest.clone();
        handles.push(tokio::spawn(async move {
            let _permit = permits.acquire().await.unwrap();
            let now = running.fetch_add(1, Ordering::SeqCst) + 1;
            highest.fetch_max(now, Ordering::SeqCst);
            sleep(Duration::from_millis(20)).await;
            running.fetch_sub(1, Ordering::SeqCst);
        }));
    }
    for handle in handles {
        handle.await.unwrap();
    }
    println!("{}", highest.load(Ordering::SeqCst));
}
```

```text
3
```

We started ten tasks, and at most three ran at once. It is used to avoid sending too many requests at once to an outside service.

## Do not lock up the worker

The most common async mistake: if a task **blocks instead of waiting**, its worker stops and no other task on that worker can run.
Let us see the difference on a single thread:

```rust
use std::time::{Duration, Instant};

async fn blocks() {
    std::thread::sleep(Duration::from_millis(100));
}

async fn waits() {
    tokio::time::sleep(Duration::from_millis(100)).await;
}

#[tokio::main(flavor = "current_thread")]
async fn main() {
    let start = Instant::now();
    tokio::join!(blocks(), blocks(), blocks());
    println!("thread sleep, at least 300 ms: {}", start.elapsed().as_millis() >= 300);

    let start = Instant::now();
    tokio::join!(waits(), waits(), waits());
    println!("tokio sleep, under 300 ms: {}", start.elapsed().as_millis() < 300);
}
```

```text
thread sleep, at least 300 ms: true
tokio sleep, under 300 ms: true
```

For heavy computing or a blocking library there is a separate thread pool:

```rust
fn heavy(n: u64) -> u64 {
    (1..=n).sum()
}

#[tokio::main]
async fn main() {
    let handle = tokio::task::spawn_blocking(|| heavy(1_000_000));
    println!("{}", handle.await.unwrap());
}
```

```text
500000500000
```

## Networking

This is the main reason tokio exists. Thousands of connections do not need thousands of threads: each connection is a task that
waits until data arrives. Here there is only a server and client running on your own computer (`127.0.0.1`); nothing goes outside.
Port `0` means "pick a free port".

```rust
use tokio::io::{AsyncReadExt, AsyncWriteExt};
use tokio::net::{TcpListener, TcpStream};

#[tokio::main]
async fn main() -> std::io::Result<()> {
    let listener = TcpListener::bind("127.0.0.1:0").await?;
    let address = listener.local_addr()?;

    tokio::spawn(async move {
        loop {
            let (mut socket, _) = listener.accept().await.unwrap();
            tokio::spawn(async move {
                let mut buffer = [0; 64];
                let n = socket.read(&mut buffer).await.unwrap();
                socket.write_all(&buffer[..n]).await.unwrap();
            });
        }
    });

    for word in ["hello", "tokio"] {
        let mut client = TcpStream::connect(address).await?;
        client.write_all(word.as_bytes()).await?;
        let mut buffer = [0; 64];
        let n = client.read(&mut buffer).await?;
        println!("{}", String::from_utf8_lossy(&buffer[..n]));
    }
    Ok(())
}
```

```text
hello
tokio
```

`AsyncReadExt` and `AsyncWriteExt` are the traits that bring `read` and `write_all`. The server starts a separate task for each
connection, so a slow client does not hold up the others.

## Async tests

`#[tokio::test]` builds a small runtime for each test:

```rust
async fn double(n: i32) -> i32 {
    tokio::task::yield_now().await;
    n * 2
}

fn main() {}

#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn doubles() {
        assert_eq!(double(4).await, 8);
    }
}

```

```text
running 1 test
test tests::doubles ... ok
test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in
```

## Summary

- `#[tokio::main]` builds a runtime and runs the async `main` with `block_on`.
- `.await` in a row is sequential; `join!` runs together in one task, `spawn` starts a new task.
- `select!` and `timeout` race; cancelling means dropping a future, and it happens at an await point.
- `mpsc` has many senders, `oneshot` one answer; `recv` does not give `None` until all senders are dropped.
- `std::sync::Mutex` is right if the lock is not held across an await; `Semaphore` limits concurrency.
- Blocking in async code: `spawn_blocking`.
