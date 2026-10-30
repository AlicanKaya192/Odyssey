## The pattern

```text
#[derive(Debug, Clone, PartialEq)]
struct Type {
    field: FieldType,
}

impl Type {
    fn new(field: FieldType) -> Self { Self { field } }
    fn read(&self) -> X { ... }
    fn change(&mut self) { ... }
    fn consume(self) -> Y { ... }
}
```

## Common derives

| Name | What it provides |
|---|---|
| `Debug` | Printing with `{:?}` |
| `Clone` | `.clone()` |
| `Copy` | A copy on assignment (only if all fields are `Copy`) |
| `PartialEq` | `==` |
| `Default` | A default value |

```rust
#[derive(Debug, Clone, Copy, PartialEq, Default)]
struct Point {
    x: i32,
    y: i32,
}

fn main() {
    let a = Point { x: 1, y: 2 };
    let b = a;
    println!("{:?} {:?}", a, b);
    println!("{}", a == b);
    println!("{:?}", Point::default());
}
```

```text
Point { x: 1, y: 2 } Point { x: 1, y: 2 }
true
Point { x: 0, y: 0 }
```

## Visibility

For now everything is in one file, so it makes no difference. Under modules (`14`) we will see the word `pub`: fields are closed to code outside the module by default.

## Field or method?

| Question | Answer |
|---|---|
| Is the value stored? | A field |
| Is it computed from other fields? | A method (`area`) |
| Must a rule be protected? | A private field plus a method |

A method can share a field's name: `rect.width` is the field, `rect.width()` the method. This is a common way to provide read-only access.
