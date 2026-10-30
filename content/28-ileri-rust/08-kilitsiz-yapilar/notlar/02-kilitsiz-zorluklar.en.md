## Three promises

| Promise | Meaning |
|---|---|
| Lock-based | If the holder stops, everyone stops |
| Lock-free | At least one branch always progresses |
| Wait-free | Each branch finishes in bounded steps |

Lock-free does not mean "fast". Under contention, retries can be slower than a lock. Its gain is that a sleeping branch keeps no one waiting.

## Memory reclamation

| Way | Idea |
|---|---|
| Never deleting | Simple, memory leaks; acceptable in a short program |
| Hazard pointers | A branch declares "I am looking at this", and the deleter waits |
| Epochs | Periods are counted, and those from old periods are deleted together |
| With `Arc` | Easy, but an atomic counter costs |

The `crossbeam-epoch` crate does this.

## How is ABA prevented?

| Way | Idea |
|---|---|
| A version counter | A growing number beside the pointer |
| Memory reclamation | If the node you look at is not deleted, the same address does not return |
| Avoiding by design | Like `take_all` |

## When to write it?

Almost never. Unless a `Mutex` is a measured bottleneck, a lock-free structure does not justify the complexity. Ready ones:

| Crate | Contents |
|---|---|
| `crossbeam` | Channels, deques, epochs |
| `dashmap` | A map with parted locks |
| `arc-swap` | Atomic `Arc` swaps |

They are not installed in this path; knowing the names is enough.

## Testing

Concurrent code cannot be verified with one run. The `loom` crate finds ordering errors by trying all orderings; if you write lock-free code, it is needed.
