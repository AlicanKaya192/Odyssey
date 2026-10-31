## One rule: whoever allocated frees

Rust and C may use different memory allocators. One freeing what the other allocated is undefined behaviour.

| Where the memory came from | How it is freed |
|---|---|
| Rust `Box::into_raw` | Rust `Box::from_raw`, through the `_free` you provide |
| Rust `CString::into_raw` | Rust `CString::from_raw` |
| C `malloc` | C `free` |
| A C library's `xyz_new` | The library's `xyz_free` |

If an undocumented C function returns a pointer, the first question is: who frees this? Freeing the result of `getenv` is wrong; the runtime library owns it.

## Errors at the boundary

C has no `Result`. An error is usually told by the return value:

| Pattern | Example |
|---|---|
| Zero success, negative error | `0`, `-1` |
| Null pointer on error | `fopen` |
| A separate error output | `int f(int *out)` |

The wrapper facing Rust turns this into `Result`, and the function facing C turns `Result` into a code. Do not pass Rust types like `Result` or `Option<&T>` across the boundary without a plan; `Option<&T>` and `Option<Box<T>>` have the same layout as a nullable pointer, but there is no such promise for the others.

## Branches and lifetimes

| Question | Why |
|---|---|
| Can the function be called from two branches at once? | If the C library does not promise it, a lock is needed |
| On which branch does a callback run? | The value may have to be `Send` |
| Does C keep the pointer? | If so, the value's lifetime is your responsibility |
| What if a handle is freed twice? | A double free, undefined behaviour |

A handle type does not get `Send` and `Sync` on its own, because raw pointers remove both. If you can promise it, write `unsafe impl`.

## Tools

| Tool | Direction | Its job |
|---|---|---|
| `bindgen` | C → Rust | Produces `extern` declarations from a header |
| `cbindgen` | Rust → C | Produces a C header from code |
| The `cc` crate | C → Rust | Compiles C sources in `build.rs` |
| The `libc` crate | C → Rust | Ready C library declarations |
| `pyo3` | Python ↔ Rust | Writing a Python module |

They are not installed in this path; knowing their names is enough.

## Linking

| Need | Written as |
|---|---|
| Naming the library | `#[link(name = "z")]` |
| From `build.rs` | `cargo:rustc-link-lib=z` |
| A search path | `cargo:rustc-link-search=path` |

## Varying numbers of arguments

Functions like `printf` are declared as `fn printf(format: *const c_char, ...) -> c_int;`. There is no check: if the format text and arguments do not agree, it is undefined behaviour. Also, in some C libraries these functions are defined inside headers and cannot be linked. Avoid them if possible.
