## A test skeleton

```rust
fn add(a: i32, b: i32) -> i32 {
    a + b
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn adds() {
        assert_eq!(add(2, 3), 5);
        assert_ne!(add(2, 3), 6);
        assert!(add(0, 0) == 0);
    }
}

fn main() {}

```

{{F_skeleton}}

## Checking macros

| Macro | Fails if |
|---|---|
| `assert!(k)` | `k` is `false` |
| `assert_eq!(a, b)` | `a != b` |
| `assert_ne!(a, b)` | `a == b` |

All three take a message at the end: `assert!(ok, "expected: {}", x)`.

## What to test?

| Case | Example |
|---|---|
| Ordinary | A single match |
| Empty | Empty text, empty list |
| Boundary | First line, last line, a value right at the limit |
| Bad input | Missing argument, a broken number |
| Distinction | Upper and lower case |

## Break the code on purpose

The question to ask when writing a test: **would this test fail if the code broke?** For example, replace `contains` with `==`: a test trying only an exact match keeps passing and misses the bug.

## What a test should not do

- Look at what was printed: test the function that returns a value.
- Depend on real files: give the text directly.
- Depend on each other: tests run at the same time and in no order.

## More

`#[should_panic]`, the `tests/` folder and code examples in documentation come in the next module.
