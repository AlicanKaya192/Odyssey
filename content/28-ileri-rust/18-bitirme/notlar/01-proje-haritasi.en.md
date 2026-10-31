## Who wakes whom?

| Event | Who | Whom |
|---|---|---|
| Time is up | The timer branch | The `Sleep`'s task |
| A message came | `send` | The task waiting on `recv` |
| The last sender dropped | `Drop` | The task waiting on `recv` |
| A task finished | The `spawn` wrapper | The task waiting on `JoinHandle` |
| A waker was called | `Task::wake` | Puts the task on the queue |
| A task is on the queue | `run` | Polls the task |

## A message's journey

1. The receiver says `recv().await`, the queue is empty, the waker is stored, and the task returns `Pending` and leaves the queue.
2. The sender calls `send`, puts the message, and takes the waker.
3. The lock is released, and `wake` is called.
4. `Task::wake` puts the task on the queue.
5. `run` takes the task and polls it; `recv` returns the message this time.

Meanwhile the receiving task uses no processor at all.

## Promises the types carry

| Type | Promise | How |
|---|---|---|
| `Producer` | One producer | Not copyable, `push(&mut self)` |
| `Consumer` | One consumer | Not copyable, `pop(&mut self)` |
| `Recv` | One waiting receiver | `recv(&mut self)` |
| `Spawner` | Tasks are `Send` | `F: Send + 'static` |
| `Ring<T, N>` | `T` can change branches | `T: Send` |

## The ring's states

| State | Condition |
|---|---|
| Empty | `head == tail` |
| Full | `tail - head == N` |
| Item count | `tail - head` |
| Slot to read | `head % N` |
| Slot to write | `tail % N` |

The counters are never reset, and the code uses plain subtraction. A lifetime is not enough to fill a 64-bit `usize`, so overflow is no practical problem.

## Ordering rules

| Operation | Ordering | Why |
|---|---|---|
| Reading your own counter | `Relaxed` | Only you write it |
| Reading the other's counter | `Acquire` | To see what was written |
| Writing your own counter | `Release` | To show what you wrote |
