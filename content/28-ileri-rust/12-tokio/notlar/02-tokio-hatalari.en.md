## Symptom and cause

| Symptom | Cause | Fix |
|---|---|---|
| `futures do nothing unless you .await or poll them` | `.await` forgotten, the body never ran | `work().await` |
| `future cannot be sent between threads safely` | An `Rc` or `MutexGuard` was held across an await | Release the lock before the await, use `Arc` |
| `` `x` does not live long enough`` | Lent to `spawn` | `async move`, `Arc` |
| The program does not end | A sender of the channel is alive | `drop(sender)` |
| Tasks run one at a time | A blocking call in async code | `spawn_blocking`, `tokio::time::sleep` |
| The program ended before the result was written | A spawned task was not waited for | `handle.await` |

## If a task is not waited for

When `main` ends the runtime shuts down and unfinished tasks are dropped. You wait for a task whose result you want.

## A receiver waiting on an empty channel

When the channel is empty, `recv` does not mean `None`; it means waiting. `None` only comes when all senders are dropped:

```rust
use std::time::Duration;
use tokio::sync::mpsc;
use tokio::time::timeout;

#[tokio::main]
async fn main() {
    let (sender, mut receiver) = mpsc::channel(8);
    sender.send(1).await.unwrap();
    println!("{:?}", receiver.recv().await);
    let waited = timeout(Duration::from_millis(50), receiver.recv()).await;
    println!("{}", waited.is_err());
    drop(sender);
    println!("{:?}", receiver.recv().await);
}
```

```text
Some(1)
true
None
```

The second line waited and timed out, because `sender` was still alive. After `drop`, `None` came right away.

## Is it cancel safe?

`select!` drops the losing branch. If the branch is in the middle of a job, the job is left half done. If being cut off at an `await` point does no harm, it is called **cancel safe**.

| Call | Cancel safe? |
|---|---|
| `mpsc::Receiver::recv` | Yes, no message is lost |
| `sleep` | Yes |
| `AsyncReadExt::read` | Yes |
| `AsyncWriteExt::write_all` | No, part of it may have been written |

Tokio's documentation says this for each method.
