## A sleeping block_on

| Step | Code |
|---|---|
| Build the waker | `Waker::from(Arc::new(ThreadWaker(thread::current())))` |
| Build the context | `Context::from_waker(&waker)` |
| Fix it | `pin!(future)` |
| Poll | `future.as_mut().poll(&mut cx)` |
| `Pending` | `thread::park()` |
| `Ready(v)` | `return v` |

## Waker rules

| Rule | Why |
|---|---|
| A future returning `Pending` guarantees a wake | Otherwise it hangs |
| The latest poll's waker is the valid one | A future can move to another task |
| Checking and storing under the same lock | Otherwise the wake is lost |
| `wake` after releasing the lock | The woken work need not wait for the lock |
| `wake` may be called many times | An extra poll is harmless |
| `wake` must return quickly | It should not hold up the calling branch |

## wake and wake_by_ref

| Method | Difference |
|---|---|
| `waker.wake()` | Consumes the waker; for when it is not needed again |
| `waker.wake_by_ref()` | Borrows |
| `waker.clone()` | A copy for storing |

## A small executor

| Part | Code |
|---|---|
| Queue | `channel()` |
| Task | `Task { future: Mutex<Option<BoxFuture>>, queue: Sender<Arc<Task>> }` |
| Waking | `queue.send(self)` |
| Loop | `while let Ok(task) = queue.recv()` |
| End | When all `Sender`s drop |

`BoxFuture` = `Pin<Box<dyn Future<Output = ()> + Send>>`. Different `async fn`s have different types; `dyn` is needed for them to sit on the same queue.

## Concurrency patterns

| Pattern | What it does | When one finishes |
|---|---|---|
| join | Waits for both | The result when both finish |
| select | Takes the first to finish | The other is dropped |
| spawn | An independent task | The executor runs it |
