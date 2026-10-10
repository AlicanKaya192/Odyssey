## How does Python free memory?

| Mechanism | When | What it deletes |
|---|---|---|
| Reference counting | **the moment** the count drops to zero | every object not in a cycle |
| The cyclic garbage collector (`gc`) | every now and then, by itself | cycles that cannot be reached from outside |
| Neither | — | everything that is still reachable (**a leak**) |

## Tools

| Code | What it does |
|---|---|
| `sys.getrefcount(x)` | the reference count (+1 for the call itself) |
| `gc.collect()` | collect cycles now; returns the number found |
| `gc.get_referrers(x)` | who is holding `x`? |
| `weakref.finalize(x, f, ...)` | `f` is called when `x` is deleted |
| `weakref.ref(x)` / `WeakMethod` / `WeakSet` / `WeakValueDictionary` | a reference that does not keep it alive |
| `tracemalloc.start()` | turn tracking on |
| `tracemalloc.get_traced_memory()` | `(current, peak)` bytes |
| `snap = tracemalloc.take_snapshot()` | a snapshot |
| `snap.compare_to(earlier, "lineno")` | growth line by line |

## Sources of leaks

| Source | Prevention |
|---|---|
| An unlimited cache / a module-level list | `lru_cache(maxsize=...)`, a time or count limit |
| A registered listener, a callback | unsubscribe; a weak reference |
| A big object captured by a closure | capture only what you need |
| A stored exception (`__traceback__`) | keep its message |
| A file or connection never closed | `with` |
| A thread that never ends | a stop signal + `join` |
| Jupyter outputs | `del`, `gc.collect()`, restart the kernel |
