## When to use an enum?

| Question | Answer |
|---|---|
| Is the value one of a few definite states? | An enum |
| Do the states carry different data? | An enum with data |
| Do all fields always exist? | A struct |
| Are you using text constants (`"red"`)? | Turn them into an enum |

Using an enum instead of text turns a spelling mistake into a compile error:

```rust
#[derive(Debug, PartialEq)]
enum Status {
    Draft,
    Published,
}

fn main() {
    let status = Status::Draft;
    println!("{}", status == Status::Published);
    println!("{:?}", status);
}
```

```text
false
Draft
```

## Enums and structs together

Most real types are a mixture of the two: common fields in a struct, the changing state in an enum.

```rust
#[derive(Debug)]
enum State {
    Pending,
    Shipped { tracking: String },
}

#[derive(Debug)]
struct Order {
    id: u32,
    state: State,
}

fn main() {
    let order = Order { id: 7, state: State::Shipped { tracking: String::from("X1") } };
    println!("{:?}", order);
    let other = Order { id: 8, state: State::Pending };
    println!("{} {:?}", other.id, other.state);
}
```

```text
Order { id: 7, state: Shipped { tracking: "X1" } }
8 Pending
```

## Numeric values

Enums made only of names can be converted to numbers:

```rust
#[derive(Clone, Copy)]
enum Level {
    Low = 1,
    High = 10,
}

fn main() {
    println!("{}", Level::Low as i32);
    println!("{}", Level::High as i32);
}
```

```text
1
10
```

## Size

An enum takes as much room as its largest variant plus a tag saying which variant it is. One very large variant makes the whole enum large. Measured on this machine:

```rust
use std::mem::size_of;

#[allow(dead_code)]
enum Small {
    A(u8),
    B,
}

#[allow(dead_code)]
enum Big {
    A(u8),
    B([u64; 100]),
}

fn main() {
    println!("{}", size_of::<Small>());
    println!("{}", size_of::<Big>());
}
```

```text
2
808
```
