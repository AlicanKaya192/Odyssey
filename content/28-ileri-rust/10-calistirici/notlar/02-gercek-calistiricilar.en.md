## What ours lacks

The executor we wrote shows the idea correctly but is not enough for real work:

| Ours | A real executor |
|---|---|
| One branch per timer | One timer branch, a sorted list of times |
| Polling on one branch | As many worker branches as cores |
| One shared queue | A queue per worker; an idle worker steals work (work stealing) |
| No network support | The operating system's event mechanism |
| A task's result cannot be taken | `spawn` returns a handle that can be awaited |

## Who wakes the network?

We opened a branch for `Timer`, but ten thousand branches for ten thousand connections would bring us back to the start. Operating systems let one branch watch thousands of sources for this:

| System | Mechanism |
|---|---|
| Linux | `epoll` |
| macOS | `kqueue` |
| Windows | IOCP |

This part of an executor is called the **reactor**. When "there is data on this connection" arrives, it calls the matching waker. The future's side does not change: it stores the waker and returns `Pending`.

## Why is it not built into the language?

A small embedded device and a big server need different things. Rust gives only the `Future` and `Waker` contract and leaves the executor to you. That is why `async` code can run even with no operating system kernel.

## Known names

| Crate | Where |
|---|---|
| `tokio` | Networks and servers; the most common |
| `smol` | Small and plain |
| `embassy` | Embedded systems |

## What about long work?

Long calculation on the executor's branch stops the other tasks. The solution is to give the work to a separate branch and await its finish as a future. Our `Timer` uses exactly this shape: the work on a branch, the message by waker. The `oneshot` exercise is the same bridge.
