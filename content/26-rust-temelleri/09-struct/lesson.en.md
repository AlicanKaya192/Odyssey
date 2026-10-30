# Structs and Methods

A user's name, age and email belong together. Rather than keeping them in separate variables we gather them in one type. A **struct** is the way to define your own type.

## Defining a struct

```rust
struct User {
    name: String,
    age: u32,
}

fn main() {
    let user = User {
        name: String::from("Ada"),
        age: 36,
    };
    println!("{} {}", user.name, user.age);
}
```

```text
Ada 36
```

- `struct` defines a new type. Type names are written in `PascalCase`.
- The `name: String` lines inside the braces are called **fields**.
- When creating a value all fields must be given, in any order.
- A field is reached with `.`.

To change one, the whole variable must be `mut`. In Rust there is no making a single field `mut`:

```rust
struct User {
    name: String,
    age: u32,
}

fn main() {
    let mut user = User {
        name: String::from("Ada"),
        age: 36,
    };
    user.age += 1;
    println!("{}", user.age);
}
```

```text
37
```

## Short forms

If a field name and a variable name match, writing it once is enough. With `..` the remaining fields are taken from another value:

```rust
struct Point {
    x: i32,
    y: i32,
    z: i32,
}

fn main() {
    let x = 1;
    let y = 2;
    let base = Point { x, y, z: 3 };
    let moved = Point { x: 10, ..base };
    println!("{} {} {}", moved.x, moved.y, moved.z);
    println!("{}", base.x);
}
```

```text
10 2 3
1
```

Note: `..base` moves fields. Here `name` was given anew and the rest are numbers, so `Copy`, and `base` is still usable. If a `String` field moved, that field of `base` could not be used.

## Ownership and structs

A struct owns its fields. A struct with a `String` field also owns the heap memory, and everything is dropped when it goes out of scope. Assignment is again a move:

```rust
struct User {
    name: String,
    age: u32,
}

fn main() {
    let first = User { name: String::from("Ada"), age: 36 };
    let second = first;
    println!("{} {}", first.age, second.age);
}
```

```text
error[E0382]: borrow of moved value: `first`
 --> main.rs:9:23
  |
7 |     let first = User { name: String::from("Ada"), age: 36 };
  |         ----- move occurs because `first` has type `User`, which does not implement
  the `Copy` trait
8 |     let second = first;
  |                  ----- value moved here
9 |     println!("{} {}", first.age, second.age);
  |                       ^^^^^^^^^ value borrowed here after move
  |
note: if `User` implemented `Clone`, you could clone the value
 --> main.rs:1:1
  |
1 | struct User {
  | ^^^^^^^^^^^ consider implementing `Clone` for this type
...
8 |     let second = first;
  |                  ----- you could clone this value
```

You may want fields to be references (`name: &str`), but that needs lifetimes, in the second module. For now make structs own their data: `String` rather than `&str`.

## Printing a struct: derive

Let us try printing a struct directly:

```rust
struct Rectangle {
    width: u32,
    height: u32,
}

fn main() {
    let rect = Rectangle { width: 3, height: 4 };
    println!("{:?}", rect);
}
```

```text
error[E0277]: `Rectangle` doesn't implement `Debug`
 --> main.rs:8:22
  |
8 |     println!("{:?}", rect);
  |               ----   ^^^^ `Rectangle` cannot be formatted using `{:?}` because it
  doesn't implement `Debug`
  |               |
  |               required by this formatting parameter
  |
  = help: the trait `Debug` is not implemented for `Rectangle`
help: consider annotating `Rectangle` with `#[derive(Debug)]`
  |
1 + #[derive(Debug)]
2 | struct Rectangle {
  |
```

The message gives both the problem and the fix. The line `#[derive(Debug)]` asks the compiler to generate the code that prints this type with `{:?}`. `{:#?}` gives a readable, multi-line form:

```rust
#[derive(Debug)]
struct Rectangle {
    width: u32,
    height: u32,
}

fn main() {
    let rect = Rectangle { width: 3, height: 4 };
    println!("{:?}", rect);
    println!("{:#?}", rect);
}
```

```text
Rectangle { width: 3, height: 4 }
Rectangle {
    width: 3,
    height: 4,
}
```

The `#[...]` form is called an **attribute**. `derive` adds many ready features in one line; we will see it in detail in the second module.

## Methods: impl

We define operations belonging to the data as **methods**. Methods are written in an `impl` block and their first parameter is `self`:

```rust
#[derive(Debug)]
struct Rectangle {
    width: u32,
    height: u32,
}

impl Rectangle {
    fn area(&self) -> u32 {
        self.width * self.height
    }

    fn is_square(&self) -> bool {
        self.width == self.height
    }
}

fn main() {
    let rect = Rectangle { width: 3, height: 4 };
    println!("{}", rect.area());
    println!("{}", rect.is_square());
}
```

```text
12
false
```

The three forms of `self` match the three parameter forms of the previous section:

| Written | Meaning | When |
|---|---|---|
| `&self` | Borrows to read | Most methods |
| `&mut self` | Borrows to change | A method that changes state |
| `self` | Takes ownership; the value is consumed | A method that transforms |

All three in an example:

```rust
struct Book {
    title: String,
    pages: u32,
}

impl Book {
    fn pages(&self) -> u32 {
        self.pages
    }

    fn add_pages(&mut self, count: u32) {
        self.pages += count;
    }

    fn into_title(self) -> String {
        self.title
    }
}

fn main() {
    let mut book = Book { title: String::from("Rust"), pages: 100 };
    book.add_pages(20);
    println!("{}", book.pages());
    let title = book.into_title();
    println!("{title}");
}
```

```text
120
Rust
```

After calling `into_title`, `book` cannot be used: ownership went to the method. In Rust a method name beginning with `into_` usually says this.

When you write `rect.area()` you need not write `&`: Rust adds the needed `&`, `&mut` or `*` itself. This **automatic referencing** makes every call look the same.

## Associated functions: new

A function in `impl` that takes no `self` is called an **associated function** and is called with `Type::name()`. `String::from` is one. Rust has no special thing called a constructor; the convention is an associated function named `new`:

```rust
#[derive(Debug)]
struct Rectangle {
    width: u32,
    height: u32,
}

impl Rectangle {
    fn new(width: u32, height: u32) -> Self {
        Self { width, height }
    }

    fn square(side: u32) -> Self {
        Self::new(side, side)
    }
}

fn main() {
    println!("{:?}", Rectangle::new(2, 5));
    println!("{:?}", Rectangle::square(4));
}
```

```text
Rectangle { width: 2, height: 5 }
Rectangle { width: 4, height: 4 }
```

`Self` is a short name for the type you are in: here `Rectangle`. A type may have several `impl` blocks.

## Tuple structs and unit structs

If field names are not needed, write a **tuple struct**. Its main use is not to confuse values with the same representation:

```rust
struct Meters(f64);
struct Feet(f64);

fn main() {
    let height = Meters(1.8);
    let wall = Feet(9.5);
    println!("{} {}", height.0, wall.0);
}
```

```text
1.8 9.5
```

`Meters` and `Feet` are both `f64`, but to the compiler they are different types. Mix them up when writing `add(a, b)` and it does not compile:

```rust
struct Meters(f64);
struct Feet(f64);

fn add(a: Meters, b: Meters) -> Meters {
    Meters(a.0 + b.0)
}

fn main() {
    let total = add(Meters(1.0), Feet(2.0));
    println!("{}", total.0);
}
```

```text
error[E0308]: mismatched types
 --> main.rs:9:34
  |
9 |     let total = add(Meters(1.0), Feet(2.0));
  |                 ---              ^^^^^^^^^ expected `Meters`, found `Feet`
  |                 |
  |                 arguments to this function are incorrect
  |
note: function defined here
 --> main.rs:4:4
  |
4 | fn add(a: Meters, b: Meters) -> Meters {
  |    ^^^            ---------
```

This is called the **newtype pattern**, and it means that a unit mistake, of the kind that once lost a spacecraft, is caught at compile time. You can also write `struct Marker;` with no fields (a unit struct); it will be useful with traits.

## Summary

- `struct` defines your own type; fields are reached with `.`; if the variable is `mut` all fields can change.
- A struct owns its fields; assignment is a move. For now use `String` in fields.
- `#[derive(Debug)]` with `{:?}` and `{:#?}` prints it.
- Methods are written in `impl`: `&self` reads, `&mut self` changes, `self` consumes.
- Functions with no `self` such as `new` are called with `Type::new()`.
- Tuple structs prevent mixing different meanings with the same representation.
