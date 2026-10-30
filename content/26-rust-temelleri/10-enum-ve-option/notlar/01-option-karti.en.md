## Which way to choose?

| Your intent | Write |
|---|---|
| Handle both cases | `match` |
| Do something only if there is a value | `if let Some(x) = ...` |
| Use a default if absent | `.unwrap_or(0)` |
| A computed default | <code>.unwrap_or_else(&#124;&#124; ...)</code> |
| The type's default | `.unwrap_or_default()` |
| Transform the value | <code>.map(&#124;x&#124; ...)</code> |
| The transform also gives an `Option` | <code>.and_then(&#124;x&#124; ...)</code> |
| Fall out of the function early | `?` (section `13`) |
| "There is certainly one here" | `.expect("reason")` |

## Examples

```rust
fn first_digit(text: &str) -> Option<u32> {
    text.chars().next().and_then(|c| c.to_digit(10))
}

fn main() {
    println!("{:?}", first_digit("7up"));
    println!("{:?}", first_digit("abc"));
    println!("{:?}", first_digit(""));
    println!("{}", first_digit("7up").map(|d| d + 1).unwrap_or(0));
    println!("{}", first_digit("x").unwrap_or_default());
}
```

```text
Some(7)
None
None
8
0
```

## Ownership and Option

A `match` on an `Option<String>` may move the value. To borrow, use `&` or `.as_ref()`:

```rust
fn main() {
    let name = Some(String::from("Ada"));
    if let Some(text) = &name {
        println!("{text}");
    }
    println!("{:?}", name);
    let length = name.as_ref().map(|t| t.len());
    println!("{:?}", length);
}
```

```text
Ada
Some("Ada")
Some(3)
```

## take and replace

`Option` is often used for changeable fields: `.take()` takes the value and leaves `None` in its place.

```rust
fn main() {
    let mut slot = Some(3);
    let taken = slot.take();
    println!("{:?} {:?}", taken, slot);
    let old = slot.replace(9);
    println!("{:?} {:?}", old, slot);
}
```

```text
Some(3) None
None Some(9)
```

This will be very useful in structures such as linked lists.

## Zero cost

Types such as `Option<&T>` and `Option<Box<T>>` take as much room as a pointer: the compiler encodes `None` as a null address. So it has the cost of `null` but not the danger:

```rust
use std::mem::size_of;

fn main() {
    println!("{}", size_of::<&i32>());
    println!("{}", size_of::<Option<&i32>>());
    println!("{}", size_of::<i32>());
    println!("{}", size_of::<Option<i32>>());
}
```

```text
8
8
4
8
```
