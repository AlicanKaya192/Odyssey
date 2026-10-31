## Build settings

In `Cargo.toml`, under `[profile.release]`:

| Setting | Effect | Price |
|---|---|---|
| `opt-level = 3` | The highest speed (the release default) | None |
| `opt-level = "s"` | A small file | A bit slower |
| `lto = "fat"` | Optimization across crates | Much longer compiling |
| `lto = "thin"` | Similar gain, cheaper | Longer compiling |
| `codegen-units = 1` | Better optimization | Longer compiling |
| `panic = "abort"` | A small file, no unwinding code | `catch_unwind` does not work |
| `strip = true` | Drops symbols, a small file | Weaker stack traces |
| `debug = true` | Symbols for a profiler | A bigger file |

What each one gains depends on the project; turn it on and measure.

## Fewer allocations

| Instead of | Try |
|---|---|
| `Vec::new()` + `push` | `Vec::with_capacity(n)` |
| `format!` in a loop | `clear()` + `write!` |
| `s.clone()` | `&s` or `&str` |
| A `String` parameter | A `&str` parameter |
| A `Vec<T>` parameter | A `&[T]` parameter |
| Text that sometimes changes | `Cow<str>` |
| A short-lived `Vec` | A given `&mut Vec`, reused |
| `collect` then walking | A direct iterator chain |

## Memory layout

| Situation | Do |
|---|---|
| An `enum` with a big variant | Put the big one in a `Box` |
| Many items, few fields used | Separate arrays (SoA) |
| A nested `Vec<Vec<T>>` table | One `Vec<T>`, `row * width + column` |
| A very small list | An array; linear search often suffices |
| A linked list | Usually `Vec` or `VecDeque` is faster |

## Choosing a data structure

| Need | Type |
|---|---|
| Ordered access, adding at the end | `Vec` |
| Adding at both ends | `VecDeque` |
| Lookup by key | `HashMap` |
| Ordered keys, ranges | `BTreeMap` |
| Taking the largest | `BinaryHeap` |

## When inline?

The compiler decides on its own within a crate. `#[inline]` mostly matters for small functions across crates. Writing it everywhere lengthens compiling and can grow the file; do not add it without measuring.
