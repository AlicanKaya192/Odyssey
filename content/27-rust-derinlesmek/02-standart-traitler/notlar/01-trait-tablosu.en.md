## Which type provides what? (measured)

```rust
use std::hash::Hash;

fn needs_copy<T: Copy>() {}
fn needs_eq<T: Eq>() {}
fn needs_ord<T: Ord>() {}
fn needs_hash<T: Hash>() {}

fn main() {
    needs_copy::<f64>();
    needs_eq::<String>();
    needs_ord::<char>();
    needs_hash::<Vec<String>>();
    println!("all compiled");
}
```

```text
all compiled
```

The function body is empty: since it compiles, we know the bound is met.

| Type | `Copy` | `Eq` | `Ord` | `Hash` |
|---|---|---|---|---|
| `i32`, `char`, `bool` | Yes | Yes | Yes | Yes |
| `f64` | Yes | No | No | No |
| `String` | No | Yes | Yes | Yes |
| `Vec<T>` | No | If `T` does | If `T` does | If `T` does |

## Conversions

| Written | When |
|---|---|
| `x as u8` | Between numbers, may cut |
| `u64::from(x)` | Lossless |
| `u8::try_from(x)` | May not fit, `Result` |
| `x.into()` | If the target type is known |
| `"5".parse::<i32>()` | From text, `Result` |
| `x.to_string()` | From `Display` to text |

## Display format options

If you use `f.pad(text)`, alignment options such as `{:>10}` work on your type too. `write!` ignores them.
