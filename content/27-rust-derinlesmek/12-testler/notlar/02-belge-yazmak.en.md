## Documentation comments

| Written | What it describes |
|---|---|
| `///` | The item below it |
| `//!` | The module or crate it is inside |

Markdown is written. Common headings: `# Examples`, `# Errors`, `# Panics`.

```rust
/// Parses a price in cents.
///
/// # Errors
///
/// Returns an error if the text is not a number.
///
/// # Examples
///
/// ```
/// assert_eq!(shop::cents("12"), Ok(12));
/// ```
pub fn cents(text: &str) -> Result<u32, String> {
    text.parse().map_err(|_| String::from("not a number"))
}
```

| Command | Job |
|---|---|
| `cargo doc --open` | Produce the documentation site and open it |
| `cargo test --doc` | Only doc tests |

Code blocks in documentation are compiled and run, so documentation does not go stale. The labels `no_run`, `ignore`, `should_panic` can be written on the code.

## Excuses for not writing tests

| Excuse | Reality |
|---|---|
| "The compiler catches it" | It catches type errors, not logic errors |
| "I tried it by hand" | Will you try again at the next change? |
| "A small function" | If small, the test is small too |
