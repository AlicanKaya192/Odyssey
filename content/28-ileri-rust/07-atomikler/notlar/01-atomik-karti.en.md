## Types

`AtomicBool`, `AtomicU8` … `AtomicU64`, `AtomicUsize`, `AtomicI32` …, `AtomicPtr<T>`. All in `std::sync::atomic`. They can be used as `static`, because `new` is `const` and operations take `&self`.

## Methods

| Call | Returns |
|---|---|
| `load(o)` | The value |
| `store(v, o)` | Nothing |
| `swap(v, o)` | The old value |
| `fetch_add(v, o)`, `fetch_sub` | The old value |
| `fetch_or`, `fetch_and`, `fetch_xor` | The old value |
| `fetch_max`, `fetch_min` | The old value |
| `compare_exchange(e, n, s, f)` | `Ok(old)` or `Err(actual)` |
| `compare_exchange_weak` | The same, may fail spuriously |
| `fetch_update(s, f, c)` | A loop with a closure |

`fetch_add` wraps on overflow; it does not panic.

## The compare_exchange pattern

```rust
let mut current = value.load(Ordering::Relaxed);
loop {
    let next = current * 2;
    match value.compare_exchange_weak(current, next, Ordering::AcqRel, Ordering::Relaxed) {
        Ok(_) => break,
        Err(actual) => current = actual,
    }
}
```

Inside a loop, `_weak` is preferred: it is faster on some processors, and even if it fails spuriously, the loop retries anyway. Without a loop, the strong one.

## Which ordering is valid where?

| Operation | Valid |
|---|---|
| `load` | `Relaxed`, `Acquire`, `SeqCst` |
| `store` | `Relaxed`, `Release`, `SeqCst` |
| `fetch_*`, `swap` | All |
| `compare_exchange` success | All |
| `compare_exchange` failure | `Relaxed`, `Acquire`, `SeqCst` |

`load(Ordering::Release)` panics: a read has nothing to "publish".

## When a lock?

| Case | Choice |
|---|---|
| A single number or flag | An atomic |
| Two values change together | A lock |
| A structure (list, map) | A lock |
| The lock is measured as a bottleneck | Think; first split into parts |
