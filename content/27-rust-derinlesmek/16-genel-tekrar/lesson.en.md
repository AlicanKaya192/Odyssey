# General Review

This module took Rust from "writing without fighting the compiler" to "building abstractions at no cost". This section teaches nothing new and joins the pieces. The quiz is mixed from the whole module, and the exercises ask for several topics at once.

## The module in one program

The program below uses most of the module. If you can explain every line, this module is done:

```rust
use std::error::Error;
use std::fmt;
use std::num::ParseIntError;
use std::sync::Mutex;
use std::thread;

#[derive(Debug)]
enum OrderError {
    NoColon(String),
    BadQuantity(ParseIntError),
}

impl fmt::Display for OrderError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            OrderError::NoColon(line) => write!(f, "no colon in {line}"),
            OrderError::BadQuantity(_) => write!(f, "bad quantity"),
        }
    }
}

impl Error for OrderError {}

impl From<ParseIntError> for OrderError {
    fn from(e: ParseIntError) -> Self {
        OrderError::BadQuantity(e)
    }
}

struct Order<'a> {
    name: &'a str,
    quantity: u32,
}

fn parse<'a>(line: &'a str) -> Result<Order<'a>, OrderError> {
    let (name, quantity) = line
        .split_once(':')
        .ok_or_else(|| OrderError::NoColon(line.to_string()))?;
    Ok(Order { name, quantity: quantity.trim().parse()? })
}

fn parse_all<'a>(lines: &[&'a str]) -> Result<Vec<Order<'a>>, OrderError> {
    lines.iter().map(|line| parse(line)).collect()
}

trait Pricing: Sync {
    fn price(&self, order: &Order) -> u32;
}

struct Flat(u32);
struct Bulk;

impl Pricing for Flat {
    fn price(&self, order: &Order) -> u32 {
        self.0 * order.quantity
    }
}

impl Pricing for Bulk {
    fn price(&self, order: &Order) -> u32 {
        if order.quantity >= 10 { order.quantity * 2 } else { order.quantity * 3 }
    }
}

fn main() -> Result<(), Box<dyn Error>> {
    let orders = parse_all(&["pen: 3", "ink: 12"])?;
    let rules: Vec<Box<dyn Pricing>> = vec![Box::new(Flat(5)), Box::new(Bulk)];

    for rule in &rules {
        let total = Mutex::new(0);
        thread::scope(|s| {
            for order in &orders {
                let (total, rule) = (&total, rule);
                s.spawn(move || *total.lock().unwrap() += rule.price(order));
            }
        });
        println!("{}", total.lock().unwrap());
    }

    let names: Vec<&str> = orders.iter().map(|order| order.name).collect();
    println!("{names:?}");

    if let Err(e) = parse_all(&["pen"]) {
        println!("{e}");
    }
    Ok(())
}
```

```text
75
33
["pen", "ink"]
no colon in pen
```

| Place | Topic |
|---|---|
| `enum OrderError`, `impl Error`, `From` | Designing errors |
| `struct Order<'a>` | Lifetimes: the text is borrowed from the line |
| `trait Pricing`, `Box<dyn Pricing>` | Traits and trait objects |
| `fn parse_all<'a>` and `collect` | Iterators, gathering Results |
| `thread::scope`, `Mutex` | Running at the same time, locks |
| `|order| ...` | Closures |

## The four most important ideas

**1. A trait writes behavior into a contract.** Generic code can use only what is written in its bound:

```rust
fn largest<T>(list: &[T]) -> &T {
    let mut best = &list[0];
    for item in list {
        if item > best {
            best = item;
        }
    }
    best
}

fn main() {
    println!("{}", largest(&[1, 2]));
}
```

```text
error[E0369]: binary operation `>` cannot be applied to type `&T`
 --> main.rs:4:17
  |
4 |         if item > best {
  |            ---- ^ ---- &T
  |            |
  |            &T
  |
help: consider restricting type parameter `T` with trait `PartialOrd`
  |
1 | fn largest<T: std::cmp::PartialOrd>(list: &[T]) -> &T {
  |             ++++++++++++++++++++++
```

**2. A lifetime is the proof of a borrow.** It does not extend the value; it tells the compiler the link between input and output:

```rust
fn longer(a: &str, b: &str) -> &str {
    if a.len() > b.len() { a } else { b }
}

fn main() {
    println!("{}", longer("a", "bb"));
}
```

```text
error[E0106]: missing lifetime specifier
 --> main.rs:1:32
  |
1 | fn longer(a: &str, b: &str) -> &str {
  |              ----     ----     ^ expected named lifetime parameter
  |
  = help: this function's return type contains a borrowed value, but the signature does
    not say whether it is borrowed from `a` or `b`
help: consider introducing a named lifetime parameter
  |
1 | fn longer<'a>(a: &'a str, b: &'a str) -> &'a str {
  |          ++++     ++          ++          ++
```

**3. Types give safety across branches.** `Rc` does not pass to a branch, because it is not `Send`. A data race is not found at run time; it does not compile:

```rust
use std::rc::Rc;
use std::thread;

fn main() {
    let shared = Rc::new(1);
    let handle = thread::spawn(move || println!("{shared}"));
    handle.join().unwrap();
}
```

```text
error[E0277]: `Rc<i32>` cannot be sent between threads safely
 --> main.rs:6:32
  |
6 |     let handle = thread::spawn(move || println!("{shared}"));
  |                  ------------- -------^^^^^^^^^^^^^^^^^^^^^
  |                  |             |
  |                  |             `Rc<i32>` cannot be sent between threads safely
  |                  |             within this `{closure@main.rs:6:32: 6:39}`
  |                  required by a bound introduced by this call
  |
  = help: within `{closure@main.rs:6:32: 6:39}`, the trait `Send` is not implemented for
    `Rc<i32>`
note: required because it's used within this closure
 --> main.rs:6:32
  |
6 |     let handle = thread::spawn(move || println!("{shared}"));
  |                                ^^^^^^^
note: required by a bound in `spawn`
```

**4. An error is a value, and it is designed.** An enum so the caller can decide by case, `From` so `?` can convert.

## Which tool?

| Need | Tool |
|---|---|
| The same code, different types, speed | Generics |
| Different types in one list | `Box<dyn Trait>` |
| A type of unknown size, recursion | `Box<T>` |
| Many owners, one branch | `Rc<T>` |
| Changing a shared value, one branch | `Rc<RefCell<T>>` |
| Many owners, many branches | `Arc<T>` |
| Changing, many branches | `Arc<Mutex<T>>` |
| Sending data between branches | `mpsc::channel` |

## A review question

Ask yourself: can you write these without looking?

- `impl Iterator for X`, and `map`, `filter`, `sum` on top.
- The difference between `Fn`, `FnMut`, `FnOnce`, and `move`.
- An `enum` error type: `Display`, `Error`, `From`.
- Work split into parts inside `thread::scope`.
- `#[should_panic]` and a test catching broken code.

If you get stuck, return to that section's notes. The exercises try this list.

## Summary

- Trait + generic: an abstraction at no cost. A trait object: a choice at run time.
- A lifetime only writes a relation; it does not extend the value.
- Choosing a smart pointer: how many owners, how many branches, does it change?
- An error type is design; tests and Clippy are habits.
