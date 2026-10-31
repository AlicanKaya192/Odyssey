## What can you do now?

Someone finishing this module can read and write Rust's lowest layers: build their own data structure with `unsafe`, write its promise into types, know why lock-free code is hard, and explain what is underneath an `async fn`.

## Good reading

| Resource | Its topic |
|---|---|
| The Rustonomicon | `unsafe`, ownership, memory |
| Rust Atomics and Locks | Atomics, locks, processors |
| Asynchronous Programming in Rust | `async` and executors |
| The Little Book of Rust Macros | Macro techniques |
| The Rust Reference | The full description of the language |

## Small project ideas

| Project | Which topics |
|---|---|
| Your own `HashMap` | `unsafe`, `Layout`, `Drop`, tests |
| A multi-worker executor | Atomics, work stealing, `Pin` |
| A `no_std` parser | `core`, a fixed buffer, const generics |
| A safe wrapper for a C library | FFI, ownership, `Drop` |
| A helper writing `#[derive]` | Procedural macros |

Write one, test it, and run it with `miri` if it has `unsafe`. Reading is not enough.

## The real ecosystem

In this path we stayed with the standard library. Crates you will often see in real projects:

| Crate | Its job |
|---|---|
| `tokio` | An async runtime, networks |
| `serde` | Serialization |
| `clap` | Command lines |
| `crossbeam` | Concurrency tools |
| `rayon` | Data parallelism |
| `axum` | A web server |
| `sqlx` | Databases |

## What you learned, what to leave

Most techniques in this module are not needed in everyday code. An atomic instead of `Mutex`, your own structure instead of `Vec`, a macro instead of a function are usually the wrong choice. The gain is not using them everywhere: it is recognizing when they are needed, reading code that uses them, and knowing where to look when a bug appears.
