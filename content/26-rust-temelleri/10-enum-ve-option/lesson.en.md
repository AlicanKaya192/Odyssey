# Enums and Option

A struct says "this **and** that": a user has a name **and** an age. Some things are "this **or** that": a payment is either cash or card. An **enum** matches this second case.

## Defining an enum

```rust
enum Light {
    Red,
    Yellow,
    Green,
}

fn advice(light: Light) -> &'static str {
    match light {
        Light::Red => "stop",
        Light::Yellow => "wait",
        Light::Green => "go",
    }
}

fn main() {
    println!("{}", advice(Light::Green));
    println!("{}", advice(Light::Red));
}
```

```text
go
stop
```

`enum` lists the possible **variants**. A variable holds only one of them at a time. Variants are reached with `Type::Variant`.

`match` is used to compare. `match` must handle every variant; we will see the details in the next section.

## Variants can carry data

This is what sets Rust enums apart from ordinary lists: each variant carries its own data.

```rust
#[derive(Debug)]
enum Payment {
    Cash,
    Card(String),
    Transfer { iban: String, amount: u32 },
}

fn main() {
    let payments = [
        Payment::Cash,
        Payment::Card(String::from("1234")),
        Payment::Transfer { iban: String::from("TR00"), amount: 50 },
    ];
    for p in &payments {
        println!("{:?}", p);
    }
}
```

```text
Cash
Card("1234")
Transfer { iban: "TR00", amount: 50 }
```

`Cash` carries no data, `Card` carries a text and `Transfer` two fields. All of these are values of one type, so they can sit in the same list or function parameter.

If we tried this with a struct we would need a field for each variant, leave most empty and guard rules such as "if card is chosen, iban must be empty" ourselves. With an enum an **invalid state cannot be written**.

<figure class="fig"><div class="versus"><div><h4>With a struct</h4><code>kind: String, card: String, iban: String</code><br>All fields always exist. What is <code>iban</code> while a card is chosen?</div><div><h4>With an enum</h4><code>Cash | Card(String) | Transfer { .. }</code><br>Each variant carries only its own data.</div></div><figcaption>A favourite sentence of Rust programmers: make invalid states unrepresentable.</figcaption></figure>

Enums get methods with `impl` too:

```rust
#[derive(Debug)]
enum Payment {
    Cash,
    Card(String),
    Transfer { iban: String, amount: u32 },
}

impl Payment {
    fn describe(&self) -> String {
        match self {
            Payment::Cash => String::from("cash"),
            Payment::Card(number) => format!("card {number}"),
            Payment::Transfer { amount, .. } => format!("transfer of {amount}"),
        }
    }
}

fn main() {
    println!("{}", Payment::Card(String::from("1234")).describe());
    let paid = Payment::Transfer { iban: String::from("TR00"), amount: 50 };
    println!("{}", paid.describe());
}
```

```text
card 1234
transfer of 50
```

## No null, but Option

Most languages have `null` meaning "no value", and any variable can be `null`. This is one of the most common causes of program crashes: its inventor called it "my billion-dollar mistake".

Rust has no `null`. "There may be no value" is written explicitly in the type. For this the standard library has a ready enum:

```rust
enum Option<T> {
    Some(T),
    None,
}
```

`T` means "any type" (generics are in the second module). An `Option<i32>` carries either a number or nothing. `Some` and `None` can be used everywhere with no `use`:

```rust
fn main() {
    let some_number: Option<i32> = Some(5);
    let no_number: Option<i32> = None;
    println!("{:?}", some_number);
    println!("{:?}", no_number);
    println!("{}", some_number.is_some());
}
```

```text
Some(5)
None
true
```

## You cannot add a number to an Option

`Option<i32>` and `i32` are different types. Since there may be no value, the compiler forces you to look first:

```rust
fn main() {
    let a: i32 = 5;
    let b: Option<i32> = Some(3);
    println!("{}", a + b);
}
```

```text
error[E0277]: cannot add `Option<i32>` to `i32`
 --> main.rs:4:22
  |
4 |     println!("{}", a + b);
  |                      ^ no implementation for `i32 + Option<i32>`
  |
  = help: the trait `Add<Option<i32>>` is not implemented for `i32`
help: the following other types implement trait `Add<Rhs>`
 --> /rustc/58cf8f9c35b355199727627d07ae34a4e2846d67/library\core\src\ops\arith.rs:98:8
  |
  = note: `i32` implements `Add`
 ::: /rustc/58cf8f9c35b355199727627d07ae34a4e2846d67/library\core\src\ops\arith.rs:113:0
  |
  = note: in this macro invocation
 -->
 /rustc/58cf8f9c35b355199727627d07ae34a4e2846d67/library\core\src\internal_macros.rs:22:8
  |
  = note: `&i32` implements `Add<i32>`
 :::
 /rustc/58cf8f9c35b355199727627d07ae34a4e2846d67/library\core\src\internal_macros.rs:33:8
  |
  = note: `i32` implements `Add<&i32>`
 :::
 /rustc/58cf8f9c35b355199727627d07ae34a4e2846d67/library\core\src\internal_macros.rs:44:8
  |
  = note: `&i32` implements `Add`
  = note: this error originates in the macro `add_impl` (in Nightly builds, run with -Z
    macro-backtrace for more info)
```

This error looks annoying but is the full solution to the `null` problem: **forgetting that a value may be absent does not compile.** A variable of type `i32` is certain to be a number.

## Getting a value from an Option

`match` is the clearest way:

```rust
fn describe(value: Option<i32>) -> String {
    match value {
        Some(n) => format!("got {n}"),
        None => String::from("nothing"),
    }
}

fn main() {
    println!("{}", describe(Some(3)));
    println!("{}", describe(None));
}
```

```text
got 3
nothing
```

If only one case is interesting, `if let` is shorter:

```rust
fn main() {
    let value = Some(7);
    if let Some(n) = value {
        println!("{n}");
    }
    let empty: Option<i32> = None;
    if let Some(n) = empty {
        println!("{n}");
    } else {
        println!("empty");
    }
}
```

```text
7
empty
```

Ready methods solve much in one line:

```rust
fn main() {
    let full = Some(5);
    let empty: Option<i32> = None;
    println!("{}", full.unwrap_or(0));
    println!("{}", empty.unwrap_or(0));
    println!("{:?}", full.map(|x| x * 2));
    println!("{:?}", empty.map(|x| x * 2));
}
```

```text
5
0
Some(10)
None
```

| Method | `Some(5)` | `None` |
|---|---|---|
| `unwrap()` | 5 | **Panic** |
| `expect("message")` | 5 | **Panic with the message** |
| `unwrap_or(0)` | 5 | 0 |
| `is_some()` | `true` | `false` |
| <code>map(&#124;x&#124; x * 2)</code> | `Some(10)` | `None` |

`|x| x * 2` is a short function (a **closure**), covered in detail in the second module: "takes x, returns x * 2".

## Avoid unwrap

`unwrap` stops the program if there is no value:

```rust
fn main() {
    let empty: Option<i32> = None;
    println!("{}", empty.unwrap());
}
```

```text
thread 'main' panicked at main.rs:3:26:
called `Option::unwrap()` on a `None` value
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

It can be used in short examples and where you can say "there is certainly a value here", but in a real program `match`, `if let` or `unwrap_or` are better. Think about it: must the program really die if there is no value?

## The standard library returns Option

Everything that might be absent gives an `Option`. We have been using this from the start:

```rust
fn main() {
    let days = [10, 20, 30];
    println!("{:?}", days.get(1));
    println!("{:?}", days.get(9));
    println!("{:?}", "hello".find('l'));
    println!("{:?}", "hello".find('z'));
    println!("{:?}", days.first());
}
```

```text
Some(20)
None
Some(2)
None
Some(10)
```

`.get(1)` gives the element inside `Some`, and `.get(9)` gives `None` rather than panicking. So `v[9]` panics and `v.get(9)` does not.

## Summary

- An enum is "either this or that"; variants can carry their own data.
- `Option<T>` is `Some(value)` or `None`. Rust has no `null`.
- `Option<i32>` and `i32` do not mix: forgetting absence does not compile.
- To get the value use `match`, `if let`, `unwrap_or`. `unwrap` panics if there is no value.
- Functions returning possibly absent values return `Option`.
