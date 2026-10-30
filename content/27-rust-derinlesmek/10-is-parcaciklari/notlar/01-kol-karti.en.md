## Forms

| Job | Written |
|---|---|
| Open a branch | <code>thread::spawn(move &#124;&#124; ...)</code> |
| Wait | `handle.join().unwrap()` |
| Scoped | <code>thread::scope(&#124;s&#124; { s.spawn(&#124;&#124; ...); })</code> |
| Sleep | `thread::sleep(Duration::from_millis(10))` |
| A channel | `let (tx, rx) = mpsc::channel();` |
| Send | `tx.send(v).unwrap()` |
| Receive, waiting | `rx.recv()` |
| Receive, not waiting | `rx.try_recv()` |
| Timed | `rx.recv_timeout(d)` |
| Several transmitters | `tx.clone()` |
| A bounded channel | `mpsc::sync_channel(n)` |

## Which one?

| Job | Choice |
|---|---|
| Process a list in parallel | `thread::scope` |
| A long-lived background job | `spawn` |
| Gather results from several producers | A channel |
| Update shared state | `Arc<Mutex<T>>` (section 11) |
| Many network connections | async (Advanced module) |

## Errors

| Code | Meaning | Fix |
|---|---|---|
| `E0373` | The closure borrows | `move` or `scope` |
| `E0382` | A value given to a branch or sent was used | `clone` or change the order |
| `E0277` | The type is not `Send` | `Arc` rather than `Rc` |

## The core count

`thread::available_parallelism()` says how many branches make sense. Opening more branches than cores does not gain speed on CPU work.
