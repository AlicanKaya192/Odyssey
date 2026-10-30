# match and Patterns

We saw `match` in the previous section. Here we will see why it is one of Rust's most powerful tools: `match` does not just compare values; it recognises a value's **shape** and opens it.

## The rules of match

```rust
enum Coin {
    One,
    Five,
    Ten,
}

fn value(coin: Coin) -> u32 {
    match coin {
        Coin::One => 1,
        Coin::Five => 5,
        Coin::Ten => 10,
    }
}

fn main() {
    println!("{}", value(Coin::Five));
}
```

```text
5
```

Each line is called an **arm**: a **pattern** on the left, a result to the right of `=>`. Arms are tried from top to bottom and the first that holds runs. `match` is an expression and gives a value.

## You cannot forget a case

`match` must be **exhaustive**: every case must be handled. If we delete an arm:

```rust
enum Coin {
    One,
    Five,
    Ten,
}

fn value(coin: Coin) -> u32 {
    match coin {
        Coin::One => 1,
        Coin::Five => 5,
    }
}

fn main() {
    println!("{}", value(Coin::Ten));
}
```

```text
error[E0004]: non-exhaustive patterns: `Coin::Ten` not covered
  --> main.rs:8:11
   |
 8 |     match coin {
   |           ^^^^ pattern `Coin::Ten` not covered
   |
note: `Coin` defined here
  --> main.rs:1:6
   |
 1 | enum Coin {
   |      ^^^^
...
 4 |     Ten,
   |     --- not covered
   = note: the matched value is of type `Coin`
help: ensure that all possible cases are being handled by adding a match arm with a
wildcard pattern or an explicit pattern as shown
   |
10 ~         Coin::Five => 5,
11 ~         Coin::Ten => todo!(),
   |
```

The compiler names the missing case and shows the line to add. This pays off in big projects: when you add a variant to an enum, the compiler lists **all** the places that do not handle it.

To gather everything else in one arm, use `_`. `_` does not capture a value; it says "the rest":

```rust
fn describe(n: u8) -> &'static str {
    match n {
        0 => "zero",
        1 => "one",
        _ => "many",
    }
}

fn main() {
    println!("{} {} {}", describe(0), describe(1), describe(9));
}
```

```text
zero one many
```

Using `_` turns off the exhaustiveness check: when a new variant is added the compiler no longer warns. So on enums write out the variants one by one when you can.

## Opening a value

A pattern can bind the parts inside the data to variables:

```rust
enum Message {
    Quit,
    Move { x: i32, y: i32 },
    Write(String),
}

fn handle(message: Message) -> String {
    match message {
        Message::Quit => String::from("bye"),
        Message::Move { x, y } => format!("move to {x} {y}"),
        Message::Write(text) => format!("write {text}"),
    }
}

fn main() {
    println!("{}", handle(Message::Move { x: 3, y: 4 }));
    println!("{}", handle(Message::Write(String::from("hi"))));
    println!("{}", handle(Message::Quit));
}
```

```text
move to 3 4
write hi
bye
```

- `Message::Move { x, y }` opens the fields into variables of the same name.
- `Message::Write(text)` binds the value inside to `text`.
- `Message::Quit` carries no data.

With one pattern, this arm both checked the variant and opened it. In other languages you first check the type and then convert, and those two steps can drift apart.

## Kinds of patterns

```rust
fn classify(n: i32) -> &'static str {
    match n {
        0 => "zero",
        1 | 2 => "small",
        3..=9 => "medium",
        n if n < 0 => "negative",
        _ => "large",
    }
}

fn main() {
    for n in [0, 2, 7, -4, 50] {
        println!("{n}: {}", classify(n));
    }
}
```

```text
0: zero
2: small
7: medium
-4: negative
50: large
```

| Pattern | Meaning |
|---|---|
| `0` | Exactly this value |
| <code>1 &#124; 2</code> | This or that |
| `3..=9` | In this range |
| `n if n < 0` | Adds a **guard** condition |
| `n` | Binds the rest |

`|` here means "or". An `if` added to an arm is called a **guard**: even if the pattern holds, when the condition fails the next arm is tried. Guarded arms do not count towards exhaustiveness, which is why there is still an `n` at the end.

Tuples and structs open too:

```rust
struct Point {
    x: i32,
    y: i32,
    z: i32,
}

fn main() {
    let pair = (3, 0);
    match pair {
        (0, 0) => println!("origin"),
        (x, 0) => println!("on x at {x}"),
        (_, y) => println!("y is {y}"),
    }
    let point = Point { x: 1, y: 2, z: 3 };
    let Point { x, .. } = point;
    println!("{x} {} {}", point.y, point.z);
}
```

```text
on x at 3
1 2 3
```

`..` skips the remaining fields. `(x, 0)` is "any tuple whose second item is 0".

## Matching by borrowing

Ownership applies here too. Opening a value containing a `String` with `match` moves it:

```rust
fn main() {
    let value = Some(String::from("hi"));
    match value {
        Some(text) => println!("{text}"),
        None => println!("none"),
    }
    println!("{:?}", value);
}
```

```text
error[E0382]: borrow of partially moved value: `value`
 --> main.rs:7:22
  |
4 |         Some(text) => println!("{text}"),
  |              ---- value partially moved here
...
7 |     println!("{:?}", value);
  |                      ^^^^^ value borrowed here after partial move
  |
  = note: partial move occurs because value has type `String`, which does not implement
    the `Copy` trait
help: borrow this binding in the pattern to avoid moving the value
  |
4 |         Some(ref text) => println!("{text}"),
  |              +++
```

The fix is to lend the value: `match &value`. Then `text` is a `&String`:

```rust
fn main() {
    let value = Some(String::from("hi"));
    match &value {
        Some(text) => println!("{}", text.len()),
        None => println!("none"),
    }
    println!("{:?}", value);
}
```

```text
2
Some("hi")
```

To change it, use `&mut`:

```rust
fn main() {
    let mut value = Some(String::from("hi"));
    if let Some(text) = &mut value {
        text.push_str(" there");
    }
    println!("{:?}", value);
}
```

```text
Some("hi there")
```

## if let and let else

When only one case is interesting, `match` is too long:

```rust
fn main() {
    let mut stack = vec![1, 2, 3];
    if let Some(top) = stack.last() {
        println!("top {top}");
    }
    while let Some(item) = stack.pop() {
        println!("popped {item}");
    }
}
```

```text
top 3
popped 3
popped 2
popped 1
```

`while let` is the loop form: it goes on as long as the pattern holds. `let else` says "if the pattern fails, leave at once" and reduces nesting:

```rust
fn parse_pair(text: &str) -> String {
    let Some((key, value)) = text.split_once('=') else {
        return String::from("no equals sign");
    };
    format!("{key} is {value}")
}

fn main() {
    println!("{}", parse_pair("a=1"));
    println!("{}", parse_pair("oops"));
}
```

```text
a is 1
no equals sign
```

| Form | When |
|---|---|
| `match` | Several cases, all important |
| `if let` | One case matters |
| `let else` | Leave early if it fails, so the rest stays flat |
| `while let` | Repeat as long as the pattern holds |

## The matches! macro

When only a `bool` is needed:

```rust
fn main() {
    let grade = 'B';
    println!("{}", matches!(grade, 'A' | 'B'));
    println!("{}", matches!(Some(3), Some(n) if n > 5));
}
```

```text
true
false
```

## Summary

- `match` is exhaustive: forgetting a case gives `E0004`. When an enum grows the compiler shows what is missing.
- A pattern recognises and opens a value: `Some(x)`, `Move { x, y }`, `(a, 0)`.
- `|`, `..=` and `if` guards extend patterns. `_` takes the rest.
- `match &value` opens by borrowing and does not move.
- `if let`, `let else` and `while let` are short forms; `matches!` gives a `bool`.
