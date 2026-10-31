## What could be added

| Feature | Idea |
|---|---|
| `block_on` | For one future in `main`, returning its result |
| A bounded channel | When full, `send` becomes a future too, and the sender waits |
| `select` | The `Select` from section 10, with channels and `Sleep` |
| A timeout | `select(future, timers.sleep(ms))` |
| Task cancellation | Not queueing the task when `JoinHandle` drops |
| Two worker branches | Sharing the `Receiver` inside `Arc<Mutex<...>>` |

Sorted from easy to hard. Each is small, but do not trust it without tests: passing once proves nothing in concurrent code.

## Where does a real runtime differ?

| Topic | Ours | The real one |
|---|---|---|
| Network | None | The OS event mechanism |
| Queue | An `mpsc` channel | A lock-free queue per worker |
| Workers | One branch | As many as cores, work stealing |
| Task | `Arc<Task>` + `Mutex` | A single-allocation task, a state machine |
| Timer | `BinaryHeap` | A timer wheel |
| Fairness | Queue order | A budget per task |

## Finding mistakes

| Tool | What it finds |
|---|---|
| `cargo test` | Logic mistakes |
| `miri` | Undefined behaviour in `unsafe` |
| `loom` | Tries all orderings |
| `ThreadSanitizer` | Data races |

They are not installed in this path; knowing their names is enough. If you really publish a structure like `Ring`, `miri` and `loom` count as required.

## Should this code be used in production?

No. Its aim is teaching. In production, libraries working for years such as `tokio` and `crossbeam` are used. But now when you read their documentation, `Waker`, `Pin`, `Send` or `Acquire` will not feel foreign, and when debugging you will know where to look. That, not the code, is the gain.
