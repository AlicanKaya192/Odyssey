# Capstone: A Command-Line Tool

We now combine what you have learned in one real program: a small tool that looks for a word in a file. Its name is `search`, a very small relative of `grep` on Linux.

```text
search rust notes.txt --ignore-case
```

It will write lines with their numbers. The exit codes are like `grep` too:

| Code | Meaning |
|---|---|
| `0` | Found |
| `1` | Not found |
| `2` | Error (missing argument, unreadable file) |

An **exit code** is the number a program leaves to the operating system when it ends. `0` means "no problem", and other programs decide by looking at it.

Everything new is small: reading arguments, reading a file, writing to stderr and writing tests.

## Arguments

What is written after the program's name is read with `std::env::args`:

```rust
use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();
    println!("{} values", args.len());
    println!("{}", args[1]);
    println!("{}", args[2]);
}
```

```text
3 values
rust
notes.txt
```

`env::args()` gives an iterator, and `collect` gathers it into a `Vec<String>`. **The first element is the program's own path**; the real arguments start at `args[1]`. That is why the code above counts with `args.len()` and does not print the first element: the path differs per machine.

## Reading a file

`std::fs::read_to_string` gives a whole file as a `String`. The file may not exist, so it returns `Result`:

```rust
use std::fs;

fn main() {
    match fs::read_to_string("notes.txt") {
        Ok(text) => {
            for line in text.lines() {
                println!("{line}");
            }
        }
        Err(_) => println!("cannot read the file"),
    }
    if fs::read_to_string("missing.txt").is_err() {
        println!("missing.txt: cannot read the file");
    }
}
```

```text
Rust is fast
Python is easy
rust has no garbage collector
missing.txt: cannot read the file
```

`text.lines()` splits text into lines. The line ending is not part of a line, and that includes the `\r\n` on Windows.

We did not print the error's own message, because it changes with the operating system's language. The program writes only its own sentence. In a real tool you can add the system's message next to your sentence with `{e}`.

## Settings: Config

A struct rather than scattered variables. Parsing arguments is also a function separate from `main`, because a separate function can be tested:

```rust
struct Config {
    pattern: String,
    path: String,
    ignore_case: bool,
}

fn parse_args(args: &[String]) -> Result<Config, String> {
    if args.len() < 3 {
        return Err(String::from("usage: search <pattern> <file> [--ignore-case]"));
    }
    Ok(Config {
        pattern: args[1].clone(),
        path: args[2].clone(),
        ignore_case: args.len() > 3 && args[3] == "--ignore-case",
    })
}

```

`&[String]` is a slice: the function borrows the list. `.clone()` takes a copy of the text, because `Config` must own its text.

## Searching

The real job writes nothing to the screen. It takes input and returns a result:

```rust
fn search(pattern: &str, text: &str, ignore_case: bool) -> Vec<String> {
    let wanted = if ignore_case { pattern.to_lowercase() } else { pattern.to_string() };
    let mut found = Vec::new();
    for (index, line) in text.lines().enumerate() {
        let candidate = if ignore_case { line.to_lowercase() } else { line.to_string() };
        if candidate.contains(&wanted) {
            found.push(format!("{}: {}", index + 1, line));
        }
    }
    found
}

```

Turning text to lowercase makes the comparison ignore capitals. The found line itself is written in its original form.

## Running

`run` joins the parts. The error type is `String`, and `?` passes it upwards:

```rust
fn run(config: &Config) -> Result<usize, String> {
    let text = fs::read_to_string(&config.path)
        .map_err(|_| format!("cannot read {}", config.path))?;
    let found = search(&config.pattern, &text, config.ignore_case);
    for line in &found {
        println!("{line}");
    }
    Ok(found.len())
}

```

## main: stdout, stderr and the exit code

```rust
fn main() {
    let args: Vec<String> = env::args().collect();
    let config = match parse_args(&args) {
        Ok(config) => config,
        Err(message) => {
            eprintln!("{message}");
            process::exit(2);
        }
    };
    match run(&config) {
        Ok(0) => process::exit(1),
        Ok(_) => {}
        Err(message) => {
            eprintln!("error: {message}");
            process::exit(2);
        }
    }
}

```

There are two new things here:

| Written | What it does |
|---|---|
| `eprintln!` | Like `println!`, but writes to **stderr** |
| `process::exit(n)` | Ends the program at once with code `n` |

Results go to stdout and errors to stderr. So when `search rust notes.txt > out.txt` is written, only the results enter the file.

Let us try it:

```text
$ search Rust notes.txt
1: Rust is fast
(exit code 0)

$ search rust notes.txt --ignore-case
1: Rust is fast
3: rust has no garbage collector
(exit code 0)

$ search java notes.txt
(exit code 1)

$ search Rust
usage: search <pattern> <file> [--ignore-case]
(exit code 2)

$ search Rust missing.txt
error: cannot read missing.txt
(exit code 2)
```

## About the layout

In the code `main` is very short and the real job is in `search`. This layout is no accident:

<figure class="fig"><div class="flow"><span class="node">main</span><span class="arrow">→</span><span class="node">parse_args</span><span class="arrow">→</span><span class="node">run</span><span class="arrow">→</span><span class="node ok">search</span></div><figcaption>Input and output at the edges, work without side effects in the middle. That is also the easiest place to test.</figcaption></figure>

If the project grows, `search` and `parse_args` move to `src/lib.rs`, and only `main` stays in `main.rs`.

## First tests

Writing tests in Rust needs no extra package. A test is a function with `#[test]` written above it:

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn finds_the_line() {
        let found = search("rust", "a\nrust b", false);
        assert_eq!(found, vec!["2: rust b"]);
    }

    #[test]
    fn ignores_case_when_asked() {
        assert_eq!(search("RUST", "rust", false).len(), 0);
        assert_eq!(search("RUST", "rust", true).len(), 1);
    }
}

```

`cargo test` runs the tests (here we show only the test part):

```text
running 2 tests
test tests::finds_the_line ... ok
test tests::ignores_case_when_asked ... ok

test result: ok. 2 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in
0.00s
```

| Part | Meaning |
|---|---|
| `#[cfg(test)]` | This module exists only in a test build |
| `use super::*;` | Take everything from the parent module |
| `#[test]` | This is a test |
| `assert_eq!(a, b)` | The test fails if they are not equal |

What happens when a test fails? Let us break one on purpose:

```text
running 1 test
test tests::doubles ... FAILED

failures:

---- tests::doubles stdout ----

thread 'tests::doubles' panicked at main.rs:11:9:
assertion `left == right` failed
  left: 5
 right: 4
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace


failures:
    tests::doubles

test result: FAILED. 0 passed; 1 failed; 0 ignored; 0 measured; 0 filtered out; finished
in 0.00s
```

`left` and `right` show the real values of the two sides.

**A good test is a test that really catches a bug.** Break the code on purpose; if the test does not fail, it is not enough. The last exercise of this section measures this.

## Summary

- `env::args().collect()` gives the arguments; the first element is the program's path.
- `fs::read_to_string` reads a file and returns `Result`; `.lines()` splits into lines.
- Results to stdout (`println!`), errors to stderr (`eprintln!`), status to the exit code (`process::exit`).
- Put side-effect-free work in a separate function so it can be tested.
- `#[cfg(test)]`, `#[test]`, `assert_eq!` and `cargo test` are the four parts of writing tests.

In the last section of this module we will review everything.
