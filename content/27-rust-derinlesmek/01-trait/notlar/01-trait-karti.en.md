## Forms

| Job | Written |
|---|---|
| Define | `trait T { fn f(&self); }` |
| Default | `trait T { fn f(&self) { ... } }` |
| Implement | `impl T for S { fn f(&self) { ... } }` |
| Parameter, short | `fn g(x: &impl T)` |
| Parameter, long | `fn g<X: T>(x: &X)` |
| Several bounds | `fn g<X: T + U>(x: &X)` |
| `where` | `fn g<X>(x: &X) where X: T + U` |
| Return | `fn g() -> impl T` |
| Blanket | `impl<X: U> T for X { ... }` |
| Associated type | `trait T { type Out; }` |
| Supertrait | `trait T: Display { ... }` |
| A trait's own function | `trait T { fn new() -> Self; }` |

## Self and self

| Written | Meaning |
|---|---|
| `Self` | The implementing type |
| `self` | The value itself (ownership) |
| `&self` | A borrow for reading |
| `&mut self` | A borrow for changing |

## A supertrait

`trait Report: Display` means: "whoever wants `Report` must provide `Display` too." The default methods of `Report` can use `Display`.

```rust
use std::fmt::{self, Display};

trait Report: Display {
    fn report(&self) -> String {
        format!("[report] {self}")
    }
}

struct Score(u32);

impl Display for Score {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{} points", self.0)
    }
}

impl Report for Score {}

fn main() {
    println!("{}", Score(7).report());
}
```

```text
[report] 7 points
```

## Errors

| Code | Meaning | Fix |
|---|---|---|
| `E0046` | A method missing from the contract | Write the method |
| `E0277` | The type does not provide the trait | Write an `impl` or `derive` |
| `E0599` | The trait is not in scope | `use trait_name;` |
| `E0117` | The orphan rule | Wrap it in your own type |
| `E0308` | `impl Trait` returns two types | `Box<dyn T>` |
