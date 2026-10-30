## Result methods

| Method | For `Ok(v)` | For `Err(e)` |
|---|---|---|
| `is_ok()`, `is_err()` | `true`, `false` | `false`, `true` |
| `unwrap()` | `v` | Panic |
| `expect("m")` | `v` | Panic, with a message |
| `unwrap_or(d)` | `v` | `d` |
| `unwrap_or_default()` | `v` | The type's default |
| `ok()` | `Some(v)` | `None` |
| `err()` | `None` | `Some(e)` |
| <code>map(&#124;v&#124; ...)</code> | A new `Ok` | The same `Err` |
| <code>map_err(&#124;e&#124; ...)</code> | The same `Ok` | A new `Err` |
| `?` | `v` | Returns the `Err` |

## Compared with Option

| Job | `Option` | `Result` |
|---|---|---|
| Success | `Some(v)` | `Ok(v)` |
| Failure | `None` | `Err(e)` |
| Does it say why? | No | **Yes** |
| Conversion | `ok_or(e)` | `ok()` |

Use `Option` for an "absent" with a single reason, and `Result` for a failure whose reason matters.

## Reading several values

`collect` can produce a `Result`: if even one fails, the first error comes back.

```rust
fn numbers(line: &str) -> Result<Vec<i32>, std::num::ParseIntError> {
    line.split_whitespace()
        .map(|t| t.parse::<i32>())
        .collect()
}

fn main() {
    println!("{:?}", numbers("1 2 3"));
    println!("{}", numbers("1 x 3").is_err());
}
```

```text
Ok([1, 2, 3])
true
```

## Three common things going wrong

| Symptom | Cause | Fix |
|---|---|---|
| `the ? operator can only be used...` | The function does not return `Result` | Change the signature |
| `? couldn't convert the error` | The error types differ | `map_err` |
| `unused Result` warning | The result was ignored | `match` or `?` |
