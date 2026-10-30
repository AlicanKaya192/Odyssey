## Everyday commands

| Command | What it does |
|---|---|
| `cargo new name` | Opens a new project folder |
| `cargo init` | Turns an existing folder into a project |
| `cargo run` | Builds and runs |
| `cargo build` | Builds into `target/debug/` |
| `cargo build --release` | Builds with optimisation into `target/release/` |
| `cargo check` | Only checks; produces no program |
| `cargo test` | Runs the tests |
| `cargo fmt` | Puts the code into the standard format |
| `cargo clippy` | Finds common mistakes and poor patterns |
| `cargo doc --open` | Generates and opens the project's documentation |
| `cargo add name` | Adds a package to `Cargo.toml` |
| `cargo update` | Updates the versions in `Cargo.lock` |
| `cargo clean` | Deletes the `target` folder |

## Passing arguments to the program

`--` separates arguments between `cargo run` and your program:

```bash
cargo run -- first second
```

What comes before `--` goes to Cargo; what comes after goes to your program.

## Which files go into Git?

| File | Goes into Git? | Why |
|---|---|---|
| `src/` | Yes | Source code |
| `Cargo.toml` | Yes | The project's description |
| `Cargo.lock` | Yes for a program | So everyone gets the same versions |
| `target/` | No | Can be regenerated and grows very large |

`cargo new` knows this and writes the `target` folder into `.gitignore` itself.

## Why is target so large?

Every build leaves intermediate files. Across a few projects it can reach gigabytes. Deleting it is safe:
`cargo clean` is enough, and the next build takes a little longer.
