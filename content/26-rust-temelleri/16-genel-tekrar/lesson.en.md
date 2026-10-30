# General Review

In this module you started knowing no programming at all and came as far as Rust's hardest ideas. This section teaches nothing new; it joins the parts. The quiz mixes the whole module, and the exercises ask for several topics together.

## The module in one program

The program below uses most of the module. If you can explain each line, this module is done:

```rust
use std::collections::BTreeMap;

#[derive(Debug, PartialEq, Eq, PartialOrd, Ord, Clone, Copy)]
enum Kind {
    Income,
    Expense,
}

struct Item {
    kind: Kind,
    amount: i32,
}

fn parse(line: &str) -> Result<Item, String> {
    let (word, number) = line.split_once(' ').ok_or("no space")?;
    let amount = number.parse::<i32>().map_err(|_| format!("bad amount: {number}"))?;
    let kind = match word {
        "in" => Kind::Income,
        "out" => Kind::Expense,
        other => return Err(format!("bad kind: {other}")),
    };
    Ok(Item { kind, amount })
}

fn main() {
    let mut items = Vec::new();
    for line in ["in 100", "out 30", "out x", "gift 5", "out 20"] {
        match parse(line) {
            Ok(item) => items.push(item),
            Err(message) => println!("skipped: {message}"),
        }
    }
    let mut totals = BTreeMap::new();
    for item in &items {
        *totals.entry(item.kind).or_insert(0) += item.amount;
    }
    println!("{:?}", totals);
}
```

```text
skipped: bad amount: x
skipped: bad kind: gift
{Income: 100, Expense: 50}
```

| Line | Topic |
|---|---|
| `enum Kind` and `#[derive]` | Enums and deriving traits |
| `struct Item` | Structs |
| `fn parse(line: &str)` | Slices and borrowing |
| `-> Result<Item, String>` | Error handling |
| `split_once`, `?`, `map_err` | Text and passing errors |
| `match` | Pattern matching, every arm required |
| `BTreeMap`, `entry` | Collections |
| `for item in &items` | Walking by borrowing |

## The three most important ideas

**1. Ownership.** Each value has one owner. When the owner leaves scope, the value is deleted. Assignment moves a non-`Copy` type.

```rust
fn main() {
    let a = String::from("hi");
    let b = a;
    println!("{a} {b}");
}
```

```text
error[E0382]: borrow of moved value: `a`
 --> main.rs:4:16
  |
2 |     let a = String::from("hi");
  |         - move occurs because `a` has type `String`, which does not implement the
  `Copy` trait
3 |     let b = a;
  |             - value moved here
4 |     println!("{a} {b}");
  |                ^ value borrowed here after move
  |
help: consider cloning the value if the performance cost is acceptable
  |
3 |     let b = a.clone();
  |              ++++++++
```

**2. Borrowing.** At one time either many readers or a single writer. A reference cannot outlive its owner.

```rust
fn main() {
    let mut list = vec![1];
    let first = &list[0];
    list.push(2);
    println!("{first}");
}
```

```text
error[E0502]: cannot borrow `list` as mutable because it is also borrowed as immutable
 --> main.rs:4:5
  |
3 |     let first = &list[0];
  |                  ---- immutable borrow occurs here
4 |     list.push(2);
  |     ^^^^^^^^^^^^ mutable borrow occurs here
5 |     println!("{first}");
  |                ----- immutable borrow later used here
```

**3. Write absence in the type.** There is no `null` and no exception. If it may be absent, `Option`; if it may fail, `Result`. The compiler does not let you forget.

```rust
fn first_word(text: &str) -> Option<&str> {
    text.split_whitespace().next()
}

fn main() {
    match first_word("  hello world") {
        Some(word) => println!("{word}"),
        None => println!("empty"),
    }
    println!("{:?}", first_word("   "));
}
```

```text
hello
None
```

## Reading a compiler error

This is what you will do most often in Rust. Look in order:

| Step | Where |
|---|---|
| 1. Code | `error[E0382]` |
| 2. Place | `--> main.rs:4:20` |
| 3. Labels | `^^^ value borrowed here after move` |
| 4. Suggestion | `help: consider cloning` |

Not every suggestion is right: `clone` often makes it compile, but the real fix is borrowing. First ask "who should own this value?".

## Which one to choose?

| Question | Choice |
|---|---|
| The function will only read the value | `&T`, for text `&str`, for a list `&[T]` |
| The function will change it in place | `&mut T` |
| The function will take ownership | `T` |
| The value may be absent | `Option<T>` |
| The operation may fail | `Result<T, E>` |
| A growing list | `Vec<T>` |
| From key to value | `HashMap`, if sorted `BTreeMap` |
| One of several choices | `enum` |
| Fields that stay together | `struct` |

## Summary

The next module has traits, generic types, lifetimes and closures. They build on this module's idea of ownership; if ownership has not settled, go back to sections 06 and 07 first.
