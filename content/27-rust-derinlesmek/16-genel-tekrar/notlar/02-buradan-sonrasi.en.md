## What can you do now?

Someone finishing this module can write a real tool with the standard library: a program with its own error type, tests, a clean pass through Clippy, and work split across branches.

## Small project ideas

| Project | Which topics |
|---|---|
| A tool counting words in files, each file in a branch | `thread::scope`, `Mutex`, an error type |
| A cache of limited size | Generics, `HashMap`, tests |
| A simple expression calculator | `enum`, `Box`, recursion, iterators |
| Rules working like plugins | `Box<dyn Trait>`, closures |

Write one, and finish with `cargo clippy` and tests. Reading is not enough.

## The next module: Advanced Rust

So far you used safe Rust. The advanced module opens how the things you used are made:

| Topic | Question |
|---|---|
| `unsafe` | Who guarantees what the compiler cannot prove? |
| Memory layout, your own `Vec` | How is `Vec` written? |
| Variance, `PhantomData` | How do lifetimes interact with types? |
| Atomics, your own lock | How is `Mutex` written? |
| `async`, `Future`, `Pin` | How do thousands of tasks run on one branch? |
| Macros | Code writing code |
| FFI, `no_std` | Talking to C, running without an operating system |

## What to read at this point

- **The Rust Programming Language**: the free official book, with the same topics as the module.
- **Rust Atomics and Locks**: for locks and atomic operations.
- The `std` documentation: `cargo doc --open` also produces your own project's documentation beside it.
