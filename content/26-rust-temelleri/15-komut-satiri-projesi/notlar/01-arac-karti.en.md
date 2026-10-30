## What is new in this section

| Job | Written |
|---|---|
| Arguments | `let args: Vec<String> = env::args().collect();` |
| Read a file | `fs::read_to_string(path)` |
| Lines | `text.lines()` |
| Lowercase | `line.to_lowercase()` |
| Whether it contains | `line.contains("a")` |
| Write to stderr | `eprintln!("...")` |
| Exit | `process::exit(1)` |

## Writing a file

The tool does not write, but its sibling is here:

```rust
use std::fs;

fn main() -> Result<(), std::io::Error> {
    fs::write("out.txt", "first\nsecond\n")?;
    let text = fs::read_to_string("out.txt")?;
    println!("{}", text.lines().count());
    Ok(())
}
```

```text
2
```

| Job | Written |
|---|---|
| Write it all | `fs::write(path, text)` |
| Whether it exists | `Path::new(path).exists()` |
| Create a folder | `fs::create_dir_all(path)` |

## Standard input

To read stdin rather than a file: `io::read_to_string(io::stdin())`. It can go to the same `search` function: the benefit of keeping it free of side effects.

## Cargo commands

| Command | Job |
|---|---|
| `cargo run -- rust notes.txt` | What follows `--` is the program's arguments |
| `cargo test` | Tests |
| `cargo test parse` | Tests with `parse` in their name |
| `cargo build --release` | An optimized build |
