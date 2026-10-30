## All pattern forms

| Pattern | Example | Matches |
|---|---|---|
| A constant | `5`, `'a'`, `"hi"` | Exactly this value |
| A variable | `x` | Everything, binds to `x` |
| A wildcard | `_` | Everything, binds nothing |
| Or | <code>1 &#124; 2</code> | Either |
| A range | `1..=9`, `'a'..='z'` | What is in the range |
| A tuple | `(a, 0)` | What fits the shape |
| A struct | `Point { x, .. }` | Opens the fields |
| An enum | `Some(x)` | Opens the variant |
| An array, a slice | `[first, .., last]` | What fits the shape |
| A reference | `&x` | Resolves the reference |
| Binding | `n @ 1..=9` | Both tests and binds |

## Examples

```rust
fn describe(values: &[i32]) -> String {
    match values {
        [] => String::from("empty"),
        [one] => format!("one {one}"),
        [first, .., last] => format!("{first} to {last}"),
    }
}

fn total(values: &[i32]) -> i32 {
    match values {
        [] => 0,
        [first, rest @ ..] => first + total(rest),
    }
}

fn main() {
    println!("{}", describe(&[]));
    println!("{}", describe(&[7]));
    println!("{}", describe(&[1, 2, 3]));
    println!("{}", total(&[1, 2, 3]));
}
```

```text
empty
one 7
1 to 3
6
```

`[first, rest @ ..]` splits a list into its head and the rest; it suits recursive work very well.

## @ binding

```rust
fn main() {
    let age = 15;
    match age {
        child @ 0..=12 => println!("child {child}"),
        teen @ 13..=19 => println!("teen {teen}"),
        adult => println!("adult {adult}"),
    }
}
```

```text
teen 15
```

## Patterns are not only in match

| Place | Example |
|---|---|
| `let` | `let (a, b) = pair;` |
| Function parameters | `fn f((a, b): (i32, i32))` |
| `for` | `for (i, x) in list.iter().enumerate()` |
| `if let`, `while let` | `if let Some(x) = y` |

In `let` and parameters a pattern **must always hold** (`let Some(x) = y;` is refused; you need `let else`).
