## Traps

| Trap | Explanation |
|---|---|
| Reading, then writing | `load` then `store` are two operations, and a branch can step in |
| `Relaxed` on a flag | No promise for the data |
| Consistency across atomics | Two atomics do not change together; a lock is needed |
| Verifying only with tests | x86 gives a stricter order; the error appears on another processor |
| `load` after `fetch_add` | It may read another branch's value, not the result: use `fetch_add`'s return |

## The first trap

```rust
// WRONG: another branch can step in between.
let value = counter.load(Ordering::SeqCst);
counter.store(value + 1, Ordering::SeqCst);
```

No `Ordering` fixes this. Ordering sets only the order of appearance; it does not make two operations one.

## x86 and ARM

| Processor | Behavior |
|---|---|
| x86 | Writes appear in order; `Release`/`Acquire` are mostly free |
| ARM, RISC-V | They reorder; a `Relaxed` error really appears |

So "it works" on x86 shows nothing. The program may one day run on a phone or a new-generation laptop.

## Use what is ready

| Need | A ready type |
|---|---|
| Initializing once | `OnceLock<T>`, `LazyLock<T>` |
| Counted sharing | `Arc<T>` |
| A lock | `Mutex`, `RwLock` |
| A channel | `mpsc` |
| Making branches wait | `Barrier`, `Condvar` |

Writing your own atomic algorithm is a last resort. The standard types went through expert eyes.
