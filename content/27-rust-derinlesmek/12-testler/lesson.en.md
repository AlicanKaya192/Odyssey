# Tests, Clippy and rustfmt

Rust's tools come with the language: the test runner `cargo test`, the code checker `cargo clippy` and the formatter `cargo fmt`. Running these three is a habit in a Rust project.

## Test layout

We saw `#[test]` and `assert_eq!` in the capstone of the Fundamentals. A little more:

```rust
fn divide(a: i32, b: i32) -> i32 {
    if b == 0 {
        panic!("division by zero");
    }
    a / b
}

fn parse(text: &str) -> Result<i32, String> {
    text.parse().map_err(|_| String::from("bad"))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn divides() {
        assert_eq!(divide(6, 3), 2, "six over three");
    }

    #[test]
    #[should_panic(expected = "division by zero")]
    fn zero_panics() {
        divide(1, 0);
    }

    #[test]
    fn parses() -> Result<(), String> {
        assert_eq!(parse("7")?, 7);
        Ok(())
    }

    #[test]
    #[ignore]
    fn slow_one() {
        assert!(true);
    }
}

fn main() {}

```

```text
running 4 tests
test tests::divides ... ok
test tests::parses ... ok
test tests::slow_one ... ignored
test tests::zero_panics - should panic ... ok

test result: ok. 3 passed; 0 failed; 1 ignored; 0 measured; 0 filtered out; finished in
0.00s
```

| Written | Meaning |
|---|---|
| `assert!(k, "message {}", x)` | On failure the message is written too |
| `#[should_panic(expected = "...")]` | A panic is **expected**, and the text must appear |
| `-> Result<(), String>` | `?` can be used, and `Err` fails |
| `#[ignore]` | Skipped normally, `cargo test -- --ignored` |

## Unit and integration tests

| Kind | Place | Sees |
|---|---|---|
| Unit | `mod tests` in the same file | Private things too |
| Integration | The `tests/` folder | Only `pub` |
| Doc | Code inside `///` | Only `pub` |

In a real project all run together:

```text
    Finished `test` profile [unoptimized + debuginfo] target(s)
     Running unittests src\lib.rs (target/debug/deps/shop)

running 1 test
test tests::doubles ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in
0.00s

     Running tests\outside.rs (target/debug/deps/outside)

running 1 test
test from_outside ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in
0.00s

   Doc-tests shop

running 1 test
test src\lib.rs - double (line 3) ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in
0.00s
```

The output has three parts: `src/lib.rs` unit tests, the `tests/` integration test and `Doc-tests`. A doc test guarantees that the example in the documentation **really works**:

```rust
/// Doubles a number.
///
/// ```
/// assert_eq!(shop::double(2), 4);
/// ```
pub fn double(n: i32) -> i32 {
    n * 2
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn doubles() {
        assert_eq!(double(3), 6);
    }
}

```

`///` is a documentation comment; `cargo doc` produces a site from them.

## Commands

| Command | Job |
|---|---|
| `cargo test` | All |
| `cargo test parse` | Those with `parse` in the name |
| `cargo test --lib` | Only unit |
| `cargo test --test cli` | `tests/cli.rs` |
| `cargo test -- --nocapture` | Show `println!` output |
| `cargo test -- --test-threads=1` | In order |

Tests run **at the same time** by default. Tests touching the same file break each other.

## Clippy: an extra eye

The compiler stops wrong code. `cargo clippy` tells you about correct but poor code, and how to fix it too:

```rust
pub fn total(list: &Vec<i32>) -> i32 {
    let mut sum = 0;
    for i in 0..list.len() {
        sum += list[i];
    }
    return sum;
}

```

```text
warning: unneeded `return` statement
 --> src\lib.rs:6:5
  |
6 |     return sum;
  |     ^^^^^^^^^^
  |
  = help: for further information visit
    https://rust-lang.github.io/rust-clippy/rust-1.99.0/index.html#needless_return
  = note: `#[warn(clippy::needless_return)]` on by default
help: remove `return`
  |
6 -     return sum;
6 +     sum
  |

warning: writing `&Vec` instead of `&[_]` involves a new object where a slice will do
 --> src\lib.rs:1:20
  |
1 | pub fn total(list: &Vec<i32>) -> i32 {
  |                    ^^^^^^^^^
  |
  = help: for further information visit
    https://rust-lang.github.io/rust-clippy/rust-1.99.0/index.html#ptr_arg
  = note: `#[warn(clippy::ptr_arg)]` on by default
help: change this to
  |
1 - pub fn total(list: &Vec<i32>) -> i32 {
1 + pub fn total(list: &[i32]) -> i32 {
  |

warning: the loop variable `i` is only used to index `list`
 --> src\lib.rs:3:14
  |
3 |     for i in 0..list.len() {
  |              ^^^^^^^^^^^^^
  |
  = help: for further information visit
    https://rust-lang.github.io/rust-clippy/rust-1.99.0/index.html#needless_range_loop
  = note: `#[warn(clippy::needless_range_loop)]` on by default
help: consider using an iterator
  |
3 -     for i in 0..list.len() {
3 +     for <item> in &list {
  |

warning: `shop` (lib) generated 3 warnings (run `cargo clippy --fix --lib -p shop -- `
to apply 1 suggestion)
    Finished `dev` profile [unoptimized + debuginfo] target(s)
```

Clippy has hundreds of rules (lints). Most suggestions are instructive. Not all must be accepted: to turn one off in one place, `#[allow(clippy::needless_range_loop)]`.

In CI it is common to turn warnings into errors: `cargo clippy -- -D warnings`.

## rustfmt: one format

`cargo fmt` brings code to one format, and the debate ends:

```text
before:
pub fn add( a:i32,b:i32 )->i32{
a+b
}

after cargo fmt:
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}
```

`cargo fmt --check` changes nothing and only checks; for CI. Settings are in `rustfmt.toml`, but the default format is the same in nearly every Rust project.

## An example flow

Before saving, on one line:

```text
cargo fmt && cargo clippy && cargo test
```

## Summary

- `#[should_panic]`, a test returning `Result`, `#[ignore]`.
- Unit in the same file, integration in `tests/`, doc tests inside `///`.
- `cargo test name`, `--lib`, `-- --nocapture`. Tests run at the same time.
- `cargo clippy` tells of poor code; `cargo fmt` makes one format.
