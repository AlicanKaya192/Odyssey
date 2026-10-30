## What can you do now?

- Install Rust and open a project with Cargo.
- Read and fix ownership and borrowing errors.
- Model data with structs, enums and `match`.
- Work with `Vec`, `HashMap` and text.
- Manage errors with `Result` and `?`.
- Write a small tool split into modules and tested.

## The next module: Going Deeper in Rust

| Topic | Why |
|---|---|
| Generic types and traits | Using the same code with many types |
| Lifetimes | Returning references |
| Closures and iterators | Short and fast data processing |
| Smart pointers | `Box`, `Rc`, `RefCell` |
| Concurrency | `thread`, channels, `Arc`, `Mutex` |

## What you can try on your own

Write small but real things:

| Project | What it reinforces |
|---|---|
| A number guessing game | Input, loops, `match` |
| A to-do list (saved to a file) | Structs, files, `Result` |
| A CSV summarizer | Text, `HashMap`, errors |
| A word frequency tool | `entry`, sorting |

## Resources

The official book "The Rust Programming Language" is free, and the command `rustup doc --book` opens the copy on your computer. Standard library documents come with `rustup doc --std`. Both work offline.

## When stuck

1. Read the error text to its end.
2. `rustc --explain E0382` explains that error with an example.
3. Shrink: write the shortest code showing the error. The fix often appears there.
