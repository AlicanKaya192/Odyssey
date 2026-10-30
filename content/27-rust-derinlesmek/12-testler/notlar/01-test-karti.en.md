## A skeleton

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn name_says_the_behavior() {
        let input = 2;
        let result = double(input);
        assert_eq!(result, 4);
    }
}
```

Arrange, act, assert. A test's name tells the behavior: `empty_list_gives_none`.

## Helpers

| Job | Written |
|---|---|
| Equal | `assert_eq!(a, b, "message")` |
| Not equal | `assert_ne!(a, b)` |
| True | `assert!(k)` |
| A decimal | `assert!((a - b).abs() < 1e-9)` |
| A specific error | `assert!(matches!(r, Err(E::Bad)))` |
| Debug only | `debug_assert!(k)` |

Do not compare `f64` with `==`: `0.1 + 0.2 != 0.3`.

## What to test?

| Question | Example |
|---|---|
| Ordinary | Normal input |
| Boundary | 0, 1, empty, the largest |
| Error | Which error does invalid input give |
| Invariant | Sort, then is it sorted |
| Regression | One test per bug found |

## Common Clippy suggestions

| Code | Suggestion |
|---|---|
| `for i in 0..v.len()` | `for x in &v` |
| `x == true` | `x` |
| `return x;` at the end | `x` |
| `v.len() == 0` | `v.is_empty()` |
| A `&Vec<T>` parameter | `&[T]` |
| A `&String` parameter | `&str` |
| A needless `.clone()` | Delete it |
