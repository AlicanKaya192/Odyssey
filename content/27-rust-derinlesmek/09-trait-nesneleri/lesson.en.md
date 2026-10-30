# Trait Objects: dyn

Generic code produces a separate copy per type at compile time. But what if you want to hold **different types** in the same list? In a drawing program, circles and squares, all in the same `Vec`. Generics cannot do this, because `Vec<T>` wants a single `T`. The fix is a **trait object**: `dyn Trait`.

## The problem

```rust
trait Shape {
    fn area(&self) -> f64;
    fn name(&self) -> String;
}

struct Circle {
    r: f64,
}

struct Square {
    side: f64,
}

impl Shape for Circle {
    fn area(&self) -> f64 {
        3.0 * self.r * self.r
    }

    fn name(&self) -> String {
        String::from("circle")
    }
}

impl Shape for Square {
    fn area(&self) -> f64 {
        self.side * self.side
    }

    fn name(&self) -> String {
        String::from("square")
    }
}

fn main() {
    let shapes = vec![Circle { r: 1.0 }, Square { side: 2.0 }];
    println!("{}", shapes.len());
}
```

```text
error[E0308]: mismatched types
  --> main.rs:35:42
   |
35 |     let shapes = vec![Circle { r: 1.0 }, Square { side: 2.0 }];
   |                                          ^^^^^^^^^^^^^^^^^^^^ expected `Circle`,
   found `Square`
```

A `Vec` wants one type and there are two different structs.

## Box<dyn Trait>

`dyn Shape` means "any type providing `Shape`". Since its size is unknown, it stays behind a pointer:

```rust
trait Shape {
    fn area(&self) -> f64;
    fn name(&self) -> String;
}

struct Circle {
    r: f64,
}

struct Square {
    side: f64,
}

impl Shape for Circle {
    fn area(&self) -> f64 {
        3.0 * self.r * self.r
    }

    fn name(&self) -> String {
        String::from("circle")
    }
}

impl Shape for Square {
    fn area(&self) -> f64 {
        self.side * self.side
    }

    fn name(&self) -> String {
        String::from("square")
    }
}

fn main() {
    let shapes: Vec<Box<dyn Shape>> = vec![
        Box::new(Circle { r: 1.0 }),
        Box::new(Square { side: 2.0 }),
    ];
    for s in &shapes {
        println!("{} {}", s.name(), s.area());
    }
}
```

```text
circle 3
square 4
```

Each element called its own type's `area`. Which one to call was decided **at run time**.

## How does it work?

`&dyn Shape` and `Box<dyn Shape>` hold two addresses: to the **value** and to the **method table** (vtable). A call finds the function from the table and runs it.

Let us measure:

```rust
trait Shape {
    fn area(&self) -> f64;
    fn name(&self) -> String;
}

struct Circle {
    r: f64,
}

struct Square {
    side: f64,
}

impl Shape for Circle {
    fn area(&self) -> f64 {
        3.0 * self.r * self.r
    }

    fn name(&self) -> String {
        String::from("circle")
    }
}

impl Shape for Square {
    fn area(&self) -> f64 {
        self.side * self.side
    }

    fn name(&self) -> String {
        String::from("square")
    }
}

use std::mem::size_of;

fn main() {
    println!("{}", size_of::<Box<Circle>>());
    println!("{}", size_of::<Box<dyn Shape>>());
    println!("{}", size_of::<&dyn Shape>());
    println!("{}", size_of::<&str>());
}
```

```text
8
16
16
16
```

`Box<Circle>` is 8 bytes and `Box<dyn Shape>` is 16 bytes: the second address is for the table. This is called a **fat pointer**. `&str` is like this too: an address and a length.

## Static or dynamic?

| | Generic (`impl Trait`) | `dyn Trait` |
|---|---|---|
| The call's decision | At compile time | At run time |
| Speed | Can be inlined | One step through a table |
| Code size | A copy per type | A single copy |
| Different types in one list | **No** | **Yes** |

Let the default choice be generics. Choose `dyn` when you need to hold different types together or to shorten compile times. The difference is too small to measure in most programs.

## It works with references too

If ownership is not needed, `&dyn Trait` is enough:

```rust
trait Shape {
    fn area(&self) -> f64;
    fn name(&self) -> String;
}

struct Circle {
    r: f64,
}

struct Square {
    side: f64,
}

impl Shape for Circle {
    fn area(&self) -> f64 {
        3.0 * self.r * self.r
    }

    fn name(&self) -> String {
        String::from("circle")
    }
}

impl Shape for Square {
    fn area(&self) -> f64 {
        self.side * self.side
    }

    fn name(&self) -> String {
        String::from("square")
    }
}

fn describe(shape: &dyn Shape) -> String {
    format!("{} of area {}", shape.name(), shape.area())
}

fn main() {
    println!("{}", describe(&Circle { r: 2.0 }));
    println!("{}", describe(&Square { side: 3.0 }));
}
```

```text
circle of area 12
square of area 9
```

## Not every trait can be an object

A trait must be "dyn compatible". Since the compiler makes the call through a table, methods must work without knowing the concrete type:

```rust
trait Copyable {
    fn duplicate(&self) -> Self;
}

struct Item;

impl Copyable for Item {
    fn duplicate(&self) -> Self {
        Item
    }
}

fn main() {
    let _list: Vec<Box<dyn Copyable>> = vec![Box::new(Item)];
}
```

```text
error[E0038]: the trait `Copyable` is not dyn compatible
  --> main.rs:14:28
   |
14 |     let _list: Vec<Box<dyn Copyable>> = vec![Box::new(Item)];
   |                            ^^^^^^^^ `Copyable` is not dyn compatible
   |
note: for a trait to be dyn compatible it needs to allow building a vtable
      for more information, visit
      <https://doc.rust-lang.org/reference/items/traits.html#dyn-compatibility>
  --> main.rs:2:28
   |
 1 | trait Copyable {
   |       -------- this trait is not dyn compatible...
 2 |     fn duplicate(&self) -> Self;
   |                            ^^^^ ...because method `duplicate` references the `Self`
   type in its return type
   = help: consider moving `duplicate` to another trait
   = help: only type `Item` implements `Copyable`; consider using it directly instead.
```

| Obstacle | Reason |
|---|---|
| Returning `-> Self` | The size is unknown |
| A generic method | The table would grow endlessly |
| A function with no `self` | It is unclear which type it is |

A pattern for a fix: writing `where Self: Sized` leaves that method out of the trait object.

## Back to the real type

`dyn` forgets the type. If the type is really needed back, first a way is added to the trait, or `std::any::Any` is used:

```rust
use std::any::Any;

fn describe(value: &dyn Any) -> String {
    if let Some(n) = value.downcast_ref::<i32>() {
        return format!("number {n}");
    }
    if let Some(s) = value.downcast_ref::<String>() {
        return format!("text {s}");
    }
    String::from("unknown")
}

fn main() {
    println!("{}", describe(&5));
    println!("{}", describe(&String::from("hi")));
    println!("{}", describe(&1.5));
}
```

```text
number 5
text hi
unknown
```

Using `Any` often points to a design problem; an enum may be more correct.

## Enum or dyn?

An enum can do the same job:

```rust
enum Shape {
    Circle(f64),
    Square(f64),
}

impl Shape {
    fn area(&self) -> f64 {
        match self {
            Shape::Circle(r) => 3.0 * r * r,
            Shape::Square(s) => s * s,
        }
    }
}

fn main() {
    let shapes = vec![Shape::Circle(1.0), Shape::Square(2.0)];
    let total: f64 = shapes.iter().map(|s| s.area()).sum();
    println!("{total}");
}
```

```text
7
```

| Question | Choice |
|---|---|
| The choices are fixed, all in your hands | `enum` |
| Someone else will add new types | `dyn` |
| New operations are added often | `enum` |
| New types are added often | `dyn` |

An enum also makes no heap allocation.

## Summary

- `dyn Trait` is resolved at run time; it stays behind `Box<dyn T>` or `&dyn T`.
- A fat pointer: a value address and a method table, 16 bytes.
- It holds different types in one list. The default is still generics.
- `-> Self`, a generic method and a function with no `self` stop it being an object.
- For fixed choices an enum is better.
