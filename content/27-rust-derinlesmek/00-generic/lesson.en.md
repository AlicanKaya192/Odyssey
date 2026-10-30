# Generics

Think of two functions doing the same job: one finds the largest in an `i32` list, the other in a `char` list. Their bodies are identical word for word; only the types differ. **Generics** means writing a type like a variable: you write the code once and it works with every type.

You have in fact been using this for a while. `Vec<i32>`, `Option<String>` and `Result<i32, String>` are all generic types.

## The problem of repetition

```rust
fn largest_number(list: &[i32]) -> &i32 {
    let mut top = &list[0];
    for item in list {
        if item > top {
            top = item;
        }
    }
    top
}

fn largest_letter(list: &[char]) -> &char {
    let mut top = &list[0];
    for item in list {
        if item > top {
            top = item;
        }
    }
    top
}

fn main() {
    println!("{}", largest_number(&[3, 9, 2]));
    println!("{}", largest_letter(&['a', 'z', 'm']));
}
```

```text
9
z
```

Two functions, one idea. If you find a bug, you fix it in two places.

## A generic function

A type parameter is written in angle brackets, right after the function's name. By custom it is a short capital letter: `T` (type).

```rust
fn largest<T>(list: &[T]) -> &T {
```

It reads "`largest` works for any type `T`". But this much does not compile:

```rust
fn largest<T>(list: &[T]) -> &T {
    let mut top = &list[0];
    for item in list {
        if item > top {
            top = item;
        }
    }
    top
}

fn main() {
    println!("{}", largest(&[3, 9, 2]));
}
```

```text
error[E0369]: binary operation `>` cannot be applied to type `&T`
 --> main.rs:4:17
  |
4 |         if item > top {
  |            ---- ^ --- &T
  |            |
  |            &T
  |
help: consider restricting type parameter `T` with trait `PartialOrd`
  |
1 | fn largest<T: std::cmp::PartialOrd>(list: &[T]) -> &T {
  |             ++++++++++++++++++++++
```

The compiler is right: `T` may be any type, and not every type can be compared with `>`. It gives the suggestion too: say that `T` can be compared.

```rust
fn largest<T: PartialOrd>(list: &[T]) -> &T {
    let mut top = &list[0];
    for item in list {
        if item > top {
            top = item;
        }
    }
    top
}

fn main() {
    println!("{}", largest(&[3, 9, 2]));
    println!("{}", largest(&['a', 'z', 'm']));
    println!("{}", largest(&[1.5, 0.5]));
    let words = [String::from("pear"), String::from("apple")];
    println!("{}", largest(&words));
}
```

```text
9
z
1.5
pear
```

`T: PartialOrd` is a **bound**: "`T` may only be a type that can be compared." `PartialOrd` is a **trait**: a contract saying what a type can do. We will write traits in the next section. For now, what you must know is that generic code can use only what the bound says about `T`.

The function returns `&T` and wants no copy. That is why it works with a `String` list too, even though `String` cannot be copied.

## A generic struct

```rust
#[derive(Debug)]
struct Point<T> {
    x: T,
    y: T,
}

fn main() {
    let a = Point { x: 1, y: 2 };
    let b = Point { x: 1.5, y: 2.5 };
    println!("{:?} {:?}", a, b);
}
```

```text
Point { x: 1, y: 2 } Point { x: 1.5, y: 2.5 }
```

`x` and `y` are the same `T`. If they differ, it does not compile:

```rust
#[derive(Debug)]
struct Point<T> {
    x: T,
    y: T,
}

fn main() {
    let a = Point { x: 1, y: 2.5 };
    println!("{:?}", a);
}
```

```text
error[E0308]: mismatched types
 --> main.rs:8:30
  |
8 |     let a = Point { x: 1, y: 2.5 };
  |                              ^^^ expected integer, found floating-point number
```

If you want two types, write two parameters:

```rust
#[derive(Debug)]
struct Pair<A, B> {
    first: A,
    second: B,
}

fn main() {
    let pair = Pair { first: 1, second: "one" };
    println!("{:?}", pair);
    println!("{}", pair.second);
}
```

```text
Pair { first: 1, second: "one" }
one
```

## Generic methods

`impl` must introduce the type parameter too, or it takes `T` for a real type's name:

```rust
#[derive(Debug)]
struct Point<T> {
    x: T,
    y: T,
}

impl<T> Point<T> {
    fn new(x: T, y: T) -> Point<T> {
        Point { x, y }
    }

    fn x(&self) -> &T {
        &self.x
    }
}

impl Point<f64> {
    fn length(&self) -> f64 {
        (self.x * self.x + self.y * self.y).sqrt()
    }
}

fn main() {
    let a = Point::new(3, 4);
    println!("{}", a.x());
    let b = Point::new(3.0, 4.0);
    println!("{}", b.length());
}
```

```text
3
5
```

`impl<T> Point<T>` means "for every `T`", and `impl Point<f64>` means "only for `f64`". The method in the second block does not exist on a `Point<i32>`:

```rust
struct Point<T> {
    x: T,
    y: T,
}

impl Point<f64> {
    fn length(&self) -> f64 {
        (self.x * self.x + self.y * self.y).sqrt()
    }
}

fn main() {
    let a = Point { x: 3, y: 4 };
    println!("{}", a.length());
}
```

```text
error[E0599]: no method named `length` found for struct `Point<{integer}>` in the
current scope
  --> main.rs:14:22
   |
 1 | struct Point<T> {
   | --------------- method `length` not found for this struct
...
14 |     println!("{}", a.length());
   |                      ^^^^^^ method not found in `Point<{integer}>`
   |
   = note: the method was found for `Point<f64>`
```

A bound also goes only on the method needing it. A `Point<T>` can be created for every type, but `larger` needs `T` to be comparable:

```rust
#[derive(Debug)]
struct Point<T> {
    x: T,
    y: T,
}

impl<T: PartialOrd + Copy> Point<T> {
    fn larger(&self) -> T {
        if self.x > self.y {
            self.x
        } else {
            self.y
        }
    }
}

fn main() {
    println!("{}", Point { x: 3, y: 9 }.larger());
    println!("{}", Point { x: 'b', y: 'a' }.larger());
}
```

```text
9
b
```

## A generic enum

`Option` and `Result` are no longer a mystery. In the standard library they are written roughly like this:

```text
enum Option<T> {
    Some(T),
    None,
}

enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

You can write your own generic enum too:

```rust
#[derive(Debug)]
enum Reply<T> {
    Found(T),
    Missing,
}

fn find(list: &[i32], wanted: i32) -> Reply<usize> {
    for (index, item) in list.iter().enumerate() {
        if *item == wanted {
            return Reply::Found(index);
        }
    }
    Reply::Missing
}

fn main() {
    println!("{:?}", find(&[5, 7], 7));
    println!("{:?}", find(&[5, 7], 9));
    let text: Reply<&str> = Reply::Found("hi");
    println!("{:?}", text);
}
```

```text
Found(1)
Missing
Found("hi")
```

## Naming a type: the turbofish

The compiler usually infers `T`. If it cannot, you say it plainly. The nickname of the `::<...>` form is the **turbofish**:

```rust
fn main() {
    let n = "42".parse::<i32>().unwrap();
    let empty = Vec::<i32>::new();
    let letters = "abc".chars().collect::<Vec<_>>();
    println!("{n} {} {:?}", empty.len(), letters);
}
```

```text
42 0 ['a', 'b', 'c']
```

`_` means "you find this part": `Vec<_>`.

## Is there a cost?

No. The compiler produces generic code separately for each type you use. This is called **monomorphization**:

<figure class="fig"><div class="flow"><span class="node">largest&lt;T&gt;</span><span class="arrow">→</span><span class="node ok">largest for i32</span><span class="arrow">→</span><span class="node ok">largest for char</span></div><figcaption>When compiling ends, no generics remain; there are separate functions as if written by hand.</figcaption></figure>

There is no slowness at run time. The price: since new code is produced for each type, compiling takes a little longer and the program gets a little larger.

Let us measure a type's size too:

```rust
use std::mem::size_of;

struct Point<T> {
    x: T,
    y: T,
}

fn main() {
    println!("{}", size_of::<i32>());
    println!("{}", size_of::<Point<i32>>());
    println!("{}", size_of::<Point<f64>>());
    println!("{}", size_of::<Point<u8>>());
}
```

```text
4
8
16
2
```

A `Point<f64>` is exactly two `f64`s: it carries nothing extra.

## Const generics

Not only a type but a number can be a parameter too. It is useful because an array's size is part of its type:

```rust
fn total<const N: usize>(values: [i32; N]) -> i32 {
    let mut sum = 0;
    for v in values {
        sum += v;
    }
    sum
}

fn main() {
    println!("{}", total([1, 2, 3]));
    println!("{}", total([1, 2, 3, 4, 5]));
}
```

```text
6
15
```

`const N: usize` means "a number known at compile time". Separate copies are produced for `[i32; 3]` and `[i32; 5]`.

## Summary

- `fn f<T>(...)`, `struct S<T>`, `enum E<T>`, `impl<T> S<T>`: the type parameter is in angle brackets.
- Generic code uses only what the bound says about `T`: `T: PartialOrd`.
- `impl<T> S<T>` for every type, `impl S<f64>` only for that type.
- `::<T>` (turbofish) gives a type plainly; `_` leaves the rest to the compiler.
- Monomorphization: separate code is produced per type, with no cost at run time.
- `const N: usize` makes a number a parameter too.
