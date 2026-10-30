## Repetitive code

As an error enum grows, writing `Display` and `From` gets tedious. The Rust world has two common crates for this. **They are not installed in this path**, and the boxes below were not run here; I mention the names because you will see them in other projects.

## thiserror: for libraries

It writes the lesson's enum with a macro. The result is the same type you write by hand:

```rust
#[derive(Debug, thiserror::Error)]
enum AppError {
    #[error("bad number")]
    Parse(#[from] std::num::ParseIntError),

    #[error("age {0} is negative")]
    Negative(i64),
}
```

## anyhow: for applications

An advanced `Box<dyn Error>`. Adding context is one line:

```rust
fn read_port(text: &str) -> anyhow::Result<u16> {
    let port = text.parse().context("reading the port")?;
    Ok(port)
}
```

## By hand first

To know what the macro produces, write it by hand at least once. Everything in the lesson works with the standard library:

| By hand | Crate |
|---|---|
| `impl Display` | `#[error("...")]` |
| `impl From` | `#[from]` |
| `fn source` | `#[source]` |
| `Box<dyn Error>` | `anyhow::Error` |
| Context with `map_err` | `.context("...")` |
