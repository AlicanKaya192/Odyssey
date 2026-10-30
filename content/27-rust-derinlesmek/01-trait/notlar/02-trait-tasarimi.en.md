## Getting around the orphan rule: a wrapper

You cannot write someone else's trait for someone else's type, but you can wrap the type in your own. This is the **newtype** pattern:

```rust
use std::fmt::{self, Display};

struct Words(Vec<String>);

impl Display for Words {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "[{}]", self.0.join(", "))
    }
}

fn main() {
    let w = Words(vec![String::from("a"), String::from("b")]);
    println!("{w}");
}
```

```text
[a, b]
```

A single-field struct has no run-time cost.

## Trait or enum?

| Question | Choice |
|---|---|
| The choices are fixed and in your hands | `enum` |
| Someone else must be able to add a new type | `trait` |
| Each choice must be handled with `match` | `enum` |
| Each type should write its own behavior | `trait` |

## Why must a trait be in scope?

To call a trait's method, the trait must be brought in with `use`. So traits with same-named methods, such as `std::fmt::Write` and `std::io::Write`, do not get mixed up. The error text usually says which `use` is needed.

## Keep it small

Small traits describing one job get used in more places. Standard library examples: `Display` has one method, `Clone` two, and `Iterator` one required method and dozens of defaults.

## Same-named methods

If two traits carry the same name, you write which one you mean:

```rust
Pilot::fly(&person);
Wizard::fly(&person);
```

If the full form is needed: `<Human as Pilot>::fly(&person)`.
