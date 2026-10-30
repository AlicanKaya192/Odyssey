# Standard Traits and derive

Most of what you know in Rust is really a trait: printing `{:?}` is `Debug`, `==` is `PartialEq`, `.clone()` is `Clone`, `+` is `Add`. So you can give these abilities to your own type. The compiler writes most of them with one line.

## derive

`#[derive(...)]` tells the compiler "produce this trait's code for me":

```rust
#[derive(Debug, Clone, PartialEq)]
struct Point {
    x: i32,
    y: i32,
}

fn main() {
    let a = Point { x: 1, y: 2 };
    let b = a.clone();
    println!("{:?}", a);
    println!("{}", a == b);
}
```

```text
Point { x: 1, y: 2 }
true
```

| Trait | What it gives | Condition for derive |
|---|---|---|
| `Debug` | `{:?}` | Fields are `Debug` |
| `Clone` | `.clone()` | Fields are `Clone` |
| `Copy` | A copy on assignment | Fields are `Copy`, plus `Clone` |
| `PartialEq` | `==`, `!=` | Fields are `PartialEq` |
| `Eq` | A guarantee of full equality | `PartialEq`, no decimals |
| `PartialOrd` | `<`, `>` | `PartialEq` |
| `Ord` | A total order, `.sort()` | `Eq`, `PartialOrd` |
| `Hash` | A `HashMap` key | Fields are `Hash` |
| `Default` | `T::default()` | Fields are `Default` |

## Copy and Clone

`Clone` takes a copy plainly, and `Copy` happens by itself on assignment. `Copy` cannot be written on a type holding a `String`:

```rust
#[derive(Clone, Copy)]
struct Named {
    name: String,
}

fn main() {
    let a = Named { name: String::from("x") };
    let b = a;
    println!("{}", b.name);
}
```

```text
error[E0204]: the trait `Copy` cannot be implemented for this type
 --> main.rs:2:8
  |
1 | #[derive(Clone, Copy)]
  |                 ---- in this derive macro expansion
2 | struct Named {
  |        ^^^^^
3 |     name: String,
  |     ------------ this field does not implement `Copy`
```

The rule: `Copy` is only for types where copying the bits is enough. A type with data on the heap would get deleted twice.

## PartialEq and Eq

Why does `Partial` exist? Because of `f64`: `NaN` is not equal to itself, so the rule "every value equals itself" breaks.

```rust
fn main() {
    let nan = f64::NAN;
    println!("{}", nan == nan);
    println!("{}", 1.5 == 1.5);
    println!("{}", nan < 1.0);
    println!("{}", nan > 1.0);
}
```

```text
false
true
false
false
```

So a struct with an `f64` field cannot have `Eq`, `Ord` or `Hash`. As a result, `f64` cannot be a `HashMap` key and a `Vec<f64>` cannot be sorted with `.sort()`.

## Ordering

`derive(PartialOrd, Ord)` compares fields **in the order they are written**, and for an enum the variants in the order they are written:

```rust
#[derive(Debug, PartialEq, Eq, PartialOrd, Ord)]
enum Level {
    Low,
    High,
}

#[derive(Debug, PartialEq, Eq, PartialOrd, Ord)]
struct Task {
    level: Level,
    name: String,
}

fn main() {
    println!("{}", Level::Low < Level::High);
    let mut tasks = vec![
        Task { level: Level::High, name: String::from("b") },
        Task { level: Level::Low, name: String::from("z") },
        Task { level: Level::High, name: String::from("a") },
    ];
    tasks.sort();
    for t in &tasks {
        println!("{:?} {}", t.level, t.name);
    }
}
```

```text
true
Low z
High a
High b
```

If you want another order, write it by hand or use `sort_by_key`:

```rust
fn main() {
    let mut words = vec!["pear", "fig", "banana"];
    words.sort_by_key(|w| w.len());
    println!("{:?}", words);
    words.sort_by(|a, b| b.cmp(a));
    println!("{:?}", words);
}
```

```text
["fig", "pear", "banana"]
["pear", "fig", "banana"]
```

## Default

```rust
#[derive(Debug, Default)]
struct Settings {
    name: String,
    retries: u32,
    verbose: bool,
    limit: Option<u32>,
}

fn main() {
    println!("{:?}", Settings::default());
    let s = Settings { retries: 3, ..Default::default() };
    println!("{}", s.retries);
}
```

```text
Settings { name: "", retries: 0, verbose: false, limit: None }
3
```

`..Default::default()` means "let the remaining fields be default". A number becomes `0`, text empty, `bool` `false`, `Option` `None`.

## Display: written by hand

`Debug` is for developers and is derived. `Display` for `{}` is for users, and the compiler cannot know what you want to write, so it is **not derived**:

```rust
use std::fmt;

struct Money {
    cents: u32,
}

impl fmt::Display for Money {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "${}.{:02}", self.cents / 100, self.cents % 100)
    }
}

fn main() {
    let price = Money { cents: 1205 };
    println!("{price}");
    println!("{}", price.to_string().len());
}
```

```text
$12.05
6
```

`write!` is like `println!`, but writes the output to `f`. Writing `Display` brings `.to_string()` for free.

## From and Into

`From` defines a conversion from one type to another. Writing one brings `Into` by itself:

```rust
#[derive(Debug)]
struct Celsius(f64);

struct Fahrenheit(f64);

impl From<Fahrenheit> for Celsius {
    fn from(f: Fahrenheit) -> Celsius {
        Celsius((f.0 - 32.0) * 5.0 / 9.0)
    }
}

fn main() {
    let a = Celsius::from(Fahrenheit(212.0));
    let b: Celsius = Fahrenheit(32.0).into();
    println!("{:?} {:?}", a, b);
    println!("{:?}", u8::try_from(300).is_err());
}
```

```text
Celsius(100.0) Celsius(0.0)
true
```

`String::from("a")` is this trait. It is also what let `&str` turn into `String` when we wrote `.ok_or("text")?` in the previous module: `?` converts the error with `From`.

A conversion that may fail is `TryFrom` (`u8::try_from(300)`), and reading from text is `FromStr` (`.parse()` calls it):

```rust
use std::str::FromStr;

#[derive(Debug)]
struct Point {
    x: i32,
    y: i32,
}

impl FromStr for Point {
    type Err = String;

    fn from_str(text: &str) -> Result<Point, String> {
        let (a, b) = text.split_once(',').ok_or("no comma")?;
        let x = a.parse::<i32>().map_err(|_| "bad x")?;
        let y = b.parse::<i32>().map_err(|_| "bad y")?;
        Ok(Point { x, y })
    }
}

fn main() {
    println!("{:?}", "1,2".parse::<Point>());
    println!("{:?}", "1;2".parse::<Point>());
}
```

```text
Ok(Point { x: 1, y: 2 })
Err("no comma")
```

## Operators

`+` is really the `std::ops::Add` trait. You can write it for your own type:

```rust
use std::ops::Add;

#[derive(Debug, Clone, Copy)]
struct Vector {
    x: i32,
    y: i32,
}

impl Add for Vector {
    type Output = Vector;

    fn add(self, other: Vector) -> Vector {
        Vector { x: self.x + other.x, y: self.y + other.y }
    }
}

fn main() {
    let a = Vector { x: 1, y: 2 };
    println!("{:?}", a + a);
}
```

```text
Vector { x: 2, y: 4 }
```

`Sub`, `Mul`, `Neg` and `Index` are written the same way. Write `+` only for what is really addition: an operator should not surprise.

## Summary

- `#[derive]` produces `Debug`, `Clone`, `Copy`, `PartialEq`, `Eq`, `PartialOrd`, `Ord`, `Hash`, `Default`.
- `Copy` only on types without heap data; `f64` cannot have `Eq`, `Ord`, `Hash`.
- A derived ordering looks at field order.
- `Display` is written by hand and brings `.to_string()`.
- `From` defines a conversion, `Into` comes for free, and `?` uses it. `FromStr` is for `.parse()`.
- Operators are `std::ops` traits.
