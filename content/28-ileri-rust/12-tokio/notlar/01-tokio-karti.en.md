## Running things together

| Written as | What it does |
|---|---|
| `tokio::spawn(fut)` | A new task; gives a `JoinHandle` |
| `handle.await` | The task's result: `Result<T, JoinError>` |
| `handle.abort()` | Cancels the task |
| `tokio::join!(a, b)` | Together in one task, waits for all |
| `tokio::try_join!(a, b)` | Stops at the first `Err` |
| `tokio::select! { ... }` | Runs the first to finish, drops the others |
| `spawn_blocking(f)` | Hands a blocking job to a separate pool |
| `yield_now().await` | Gives the turn to another task |

## Time

| Written as | What it does |
|---|---|
| `sleep(d).await` | Waits without locking up the worker |
| `timeout(d, fut).await` | A `Result`: `Err(Elapsed)` when time runs out |
| `interval(d)` | `tick().await` at regular intervals |

```rust
use std::time::Duration;
use tokio::time::interval;

#[tokio::main]
async fn main() {
    let mut ticker = interval(Duration::from_millis(10));
    for n in 0..3 {
        ticker.tick().await;
        println!("tick {n}");
    }
}
```

```text
tick 0
tick 1
tick 2
```

The first `tick` returns right away.

## Choosing a channel

| Channel | Senders | Receivers | When |
|---|---|---|---|
| `mpsc` | Many | One | A job queue |
| `oneshot` | One | One, one message | An answer to a request |
| `broadcast` | Many | Many, each gets every message | Announcing events |
| `watch` | One | Many, only the latest value | Settings, state |

```rust
use tokio::sync::{broadcast, watch};

#[tokio::main]
async fn main() {
    let (sender, mut first) = broadcast::channel(8);
    let mut second = sender.subscribe();
    sender.send("news").unwrap();
    println!("{} {}", first.recv().await.unwrap(), second.recv().await.unwrap());

    let (setter, reader) = watch::channel(1);
    setter.send(2).unwrap();
    setter.send(3).unwrap();
    println!("{}", *reader.borrow());
}
```

```text
news news
3
```

## The runtime

| Written as | Meaning |
|---|---|
| `#[tokio::main]` | A multi-threaded runtime |
| `#[tokio::main(flavor = "current_thread")]` | A single thread |
| `Builder::new_multi_thread().enable_all().build()` | Building by hand |
| `runtime.block_on(fut)` | Going from normal code to async code |

`enable_all` turns on the timer and network drivers. If you forget it, `sleep` panics.

## Features

In your own project `--features full` is the easiest. If build time matters, only what is needed: `rt-multi-thread`, `macros`, `time`, `sync`, `net`, `io-util`.
