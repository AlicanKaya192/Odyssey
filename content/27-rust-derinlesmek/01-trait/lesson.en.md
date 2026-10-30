# Traits

In the previous section we wrote `T: PartialOrd`. `PartialOrd` was a **trait**: a contract saying what a type can do. A trait is close to the idea of an "interface" in other languages: "every type providing these methods suits me."

In this section we write our own trait.

## Defining a trait

A trait only lists signatures. Each type writes the body itself:

```rust
trait Describe {
    fn describe(&self) -> String;
}

struct Book {
    title: String,
}

struct Coin {
    value: u32,
}

impl Describe for Book {
    fn describe(&self) -> String {
        format!("book: {}", self.title)
    }
}

impl Describe for Coin {
    fn describe(&self) -> String {
        format!("coin worth {}", self.value)
    }
}

fn main() {
    let book = Book { title: String::from("Dune") };
    let coin = Coin { value: 5 };
    println!("{}", book.describe());
    println!("{}", coin.describe());
}
```

```text
book: Dune
coin worth 5
```

| Part | Meaning |
|---|---|
| `trait Describe` | The contract's name |
| `fn describe(&self) -> String;` | A required method, ending with a semicolon |
| `impl Describe for Book` | "`Book` provides this contract" |

If a method in the contract is forgotten, it does not compile:

```rust
trait Greeter {
    fn hello(&self) -> String;
    fn bye(&self) -> String;
}

struct Robot;

impl Greeter for Robot {
    fn hello(&self) -> String {
        String::from("beep")
    }
}

fn main() {
    println!("{}", Robot.hello());
}
```

```text
error[E0046]: not all trait items implemented, missing: `bye`
 --> main.rs:8:1
  |
3 |     fn bye(&self) -> String;
  |     ------------------------ `bye` from trait
...
8 | impl Greeter for Robot {
  | ^^^^^^^^^^^^^^^^^^^^^^ missing `bye` in implementation
```

## A default body

A trait can give a body too. A type overrides it if it wants; otherwise it comes ready:

```rust
trait Animal {
    fn name(&self) -> String;

    fn greet(&self) -> String {
        format!("Hello from {}", self.name())
    }
}

struct Dog;
struct Cat;

impl Animal for Dog {
    fn name(&self) -> String {
        String::from("Rex")
    }
}

impl Animal for Cat {
    fn name(&self) -> String {
        String::from("Tom")
    }

    fn greet(&self) -> String {
        String::from("...")
    }
}

fn main() {
    println!("{}", Dog.greet());
    println!("{}", Cat.greet());
}
```

```text
Hello from Rex
...
```

A default method can call the other methods of the same trait. `Dog` wrote only `name`, and `greet` came for free.

## Taking a trait as a parameter

A function can say "every type providing this trait". The short form is `impl Trait`:

```rust
trait Describe {
    fn describe(&self) -> String;
}

struct Book {
    title: String,
}

struct Coin {
    value: u32,
}

impl Describe for Book {
    fn describe(&self) -> String {
        format!("book: {}", self.title)
    }
}

impl Describe for Coin {
    fn describe(&self) -> String {
        format!("coin worth {}", self.value)
    }
}

fn show(item: &impl Describe) {
    println!("I see a {}", item.describe());
}

fn main() {
    show(&Book { title: String::from("Dune") });
    show(&Coin { value: 5 });
}
```

```text
I see a book: Dune
I see a coin worth 5
```

The long form of the same thing is a generic bound. The two forms do the same job, and the choice is about readability:

| Written | Difference |
|---|---|
| `fn f(x: &impl Describe)` | Short |
| `fn f<T: Describe>(x: &T)` | Can ask for the same `T` in two places |

The difference shows here: if you want `a` and `b` to be the same type, you must write generics.

```rust
fn pair_max<T: PartialOrd + Copy>(a: T, b: T) -> T {
    if a > b { a } else { b }
}

fn main() {
    println!("{}", pair_max(1, 2));
    println!("{}", pair_max('x', 'a'));
}
```

```text
2
x
```

## Several bounds and where

`+` joins bounds. When bounds get long the signature becomes unreadable, and `where` moves them down:

```rust
use std::fmt::{Debug, Display};

fn report<T, U>(item: &T, extra: &U) -> String
where
    T: Display + Clone,
    U: Debug,
{
    format!("{} {:?}", item, extra)
}

fn main() {
    println!("{}", report(&5, &"note"));
}
```

```text
5 "note"
```

## Returning impl Trait

A function can say "I return something providing this trait". The caller does not know the real type:

```rust
use std::fmt::Display;

fn make_label(n: i32) -> impl Display {
    format!("#{n}")
}

fn main() {
    let label = make_label(7);
    println!("{label}");
}
```

```text
#7
```

There is one condition: the function must return **a single** real type. For two different types you need the `dyn` of section 09:

```rust
use std::fmt::Display;

fn pick(flag: bool) -> impl Display {
    if flag {
        return 1;
    }
    "one"
}

fn main() {
    println!("{}", pick(true));
}
```

```text
error[E0308]: mismatched types
 --> main.rs:7:5
  |
3 | fn pick(flag: bool) -> impl Display {
  |                        ------------ expected a single type implementing `Display`
  because of return type
4 |     if flag {
5 |         return 1;
  |                - return type resolved to be `{integer}`
6 |     }
7 |     "one"
  |     ^^^^^ expected integer, found `&str`
  |
help: you could change the return type to be a boxed trait object
  |
3 - fn pick(flag: bool) -> impl Display {
3 + fn pick(flag: bool) -> Box<dyn Display> {
  |
help: if you change the return type to expect trait objects, box the returned
expressions
  |
5 ~         return Box::new(1);
6 |     }
7 ~     Box::new("one")
  |
```

## A bounded impl

An `impl` can be written only for types meeting a bound. This is very common in the standard library: every type providing `Display` automatically gains `.to_string()`. This is called a **blanket implementation**:

```rust
use std::fmt::Display;

trait Shout {
    fn shout(&self) -> String;
}

impl<T: Display> Shout for T {
    fn shout(&self) -> String {
        self.to_string().to_uppercase()
    }
}

fn main() {
    println!("{}", "hi".shout());
    println!("{}", 42.shout());
}
```

```text
HI
42
```

`impl<T: Display> Shout for T`: "every type providing `Display` also provides `Shout`."

## Whose trait, whose type?

To write a trait for a type, **one of the two must be yours.** You can write your own trait for `Vec`, and `Display` for your own type. You cannot write someone else's trait for someone else's type:

```rust
use std::fmt::{self, Display};

impl Display for Vec<i32> {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "list")
    }
}

fn main() {
    println!("{}", vec![1]);
}
```

```text
error[E0117]: only traits defined in the current crate can be implemented for types
defined outside of the crate
 --> main.rs:3:1
  |
3 | impl Display for Vec<i32> {
  | ^^^^^^^^^^^^^^^^^--------
  |                  |
  |                  `Vec` is not defined in the current crate
  |
  = note: impl doesn't have any local type before any uncovered type parameters
  = note: for more information see
    https://doc.rust-lang.org/reference/items/implementations.html#orphan-rules
  = note: define and implement a trait or new type instead
```

This **orphan rule** stops two libraries from writing the same thing in two different ways and clashing.

## Associated types

A trait can define a type name that the implementing type chooses. The `Item` of `Iterator` is like this (section 05):

```rust
trait Measure {
    type Output;

    fn measure(&self) -> Self::Output;
}

struct Word(String);
struct Box2(f64, f64);

impl Measure for Word {
    type Output = usize;

    fn measure(&self) -> Self::Output {
        self.0.len()
    }
}

impl Measure for Box2 {
    type Output = f64;

    fn measure(&self) -> Self::Output {
        self.0 * self.1
    }
}

fn main() {
    println!("{}", Word(String::from("rust")).measure());
    println!("{}", Box2(1.5, 2.0).measure());
}
```

```text
4
3
```

`type Output = i32;` means "for this type, `Output` is this." `Self::Output` uses it. Unlike a generic parameter, there is only **one** choice per type.

## Summary

- A `trait` is a contract, and `impl T for S` provides it. A missing method does not compile.
- A default body comes ready and can be overridden.
- `&impl T` is the short form, `<X: T>` the long form; asking for the same type in two places needs the long form.
- `+` for several bounds, `where` for long bounds.
- `-> impl T` returns a single real type.
- The orphan rule: the trait or the type must be yours.
- `type Output` is an associated type: one choice per type.
