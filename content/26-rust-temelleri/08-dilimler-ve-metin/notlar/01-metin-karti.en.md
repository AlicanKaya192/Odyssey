## Creating

| Written | Result |
|---|---|
| `String::new()` | An empty `String` |
| `String::from("a")` | A `String` from a `&str` |
| `"a".to_string()` | The same |
| `"a".to_owned()` | The same |
| `format!("{a}-{b}")` | Joins into a `String` |

All three do the same job. Most code writes `String::from` or `.to_string()`.

## Changing (needs `mut`)

| Method | What it does |
|---|---|
| `push('x')` | Adds one character |
| `push_str("xy")` | Adds text |
| `insert(0, 'x')` | Inserts at a byte position |
| `pop()` | Removes the last character |
| `clear()` | Empties it |
| `truncate(n)` | Shortens to `n` bytes |

## Querying

| Method | Returns |
|---|---|
| `len()` | The number of bytes |
| `chars().count()` | The number of letters |
| `is_empty()` | Whether it is empty |
| `contains("x")` | Whether it is inside |
| `find("x")` | The first byte position, an `Option` |
| `starts_with`, `ends_with` | Whether it starts or ends so |

## Splitting

```rust
fn main() {
    let csv = "ada,36,london";
    for part in csv.split(',') {
        println!("{part}");
    }
    let (name, rest) = csv.split_once(',').unwrap();
    println!("{name} | {rest}");
    let text = "one\ntwo";
    for line in text.lines() {
        println!("{line}");
    }
}
```

```text
ada
36
london
ada | 36,london
one
two
```

## Comparing

A `String` and a `&str` can be compared directly with `==`. It is case-sensitive.

## Numbers and text

| Direction | Written |
|---|---|
| Number to text | `42.to_string()`, `format!("{n}")` |
| Text to number | `"42".parse::<i32>()` |

Since `parse` can fail, its result is not directly a number. We will see it as `Result` in later sections.
