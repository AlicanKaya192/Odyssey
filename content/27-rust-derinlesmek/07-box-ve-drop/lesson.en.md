# Box, Deref and Drop

Values live on the stack by default, and `String` and `Vec` put their contents on the heap. A **smart pointer** is a type that holds an address and also carries extra abilities. `String` and `Vec` are already smart pointers. The simplest is `Box`.

## Box: putting on the heap

`Box::new(x)` puts a value on the heap, and only an address stays on the stack:

```rust
fn main() {
    let b = Box::new(5);
    println!("{}", b);
    println!("{}", *b + 1);
    let mut c = Box::new(String::from("hi"));
    c.push('!');
    println!("{c} {}", c.len());
}
```

```text
5
6
hi! 3
```

<figure class="fig"><svg viewBox="0 0 640 110" width="640" xmlns="http://www.w3.org/2000/svg"><text class="dim" x="20" y="24" font-size="13" font-weight="600">stack</text><text class="dim" x="390" y="24" font-size="13" font-weight="600">heap</text><g><rect class="box" x="20" y="44" width="230" height="44" rx="8"/><text class="ink" x="34" y="71" font-size="14" font-weight="600">b</text><text class="dim" x="110" y="71" font-size="12.5">Box</text></g><g><rect class="box" x="390" y="44" width="220" height="44" rx="8"/><text class="ink" x="404" y="71" font-size="14">5</text></g><path class="curve" d="M250 66 C320 66 320 66 382 66"/><polygon class="dot" points="390,66 380,61 380,71"/></svg><figcaption>Only the address (8 bytes) on the stack, the value on the heap.</figcaption></figure>

Using it is like a normal value. When a `Box` leaves scope, both it and the value on the heap are deleted.

## Why is it needed?

There are three cases:

| Case | Example |
|---|---|
| A type whose size is unknown at compile time | A recursive type |
| Moving large data without copying | Only the address moves |
| Holding a trait object without knowing its type | `Box<dyn Trait>` (section 09) |

## A recursive type

Let us write a type containing itself: a linked list. Each node holds a value and the next list.

```rust
enum List {
    Cons(i32, List),
    Nil,
}

fn main() {
    let _empty = List::Nil;
}
```

```text
error[E0072]: recursive type `List` has infinite size
 --> main.rs:1:1
  |
1 | enum List {
  | ^^^^^^^^^
2 |     Cons(i32, List),
  |               ---- recursive without indirection
  |
help: insert some indirection (e.g., a `Box`, `Rc`, or `&`) to break the cycle
  |
2 |     Cons(i32, Box<List>),
  |               ++++    +
```

The compiler cannot compute the size of `List`: `List` contains a `List`, and that a `List`... endlessly. It gives the suggestion itself: `Box`. Since an address has a fixed size, the cycle breaks:

```rust
#[derive(Debug)]
enum List {
    Cons(i32, Box<List>),
    Nil,
}

use List::{Cons, Nil};

fn sum(list: &List) -> i32 {
    match list {
        Cons(value, rest) => value + sum(rest),
        Nil => 0,
    }
}

fn main() {
    let list = Cons(1, Box::new(Cons(2, Box::new(Nil))));
    println!("{:?}", list);
    println!("{}", sum(&list));
}
```

```text
Cons(1, Cons(2, Nil))
3
```

<figure class="fig"><svg viewBox="0 0 640 168" width="640" xmlns="http://www.w3.org/2000/svg"><text class="dim" x="20" y="24" font-size="13" font-weight="600">stack</text><text class="dim" x="390" y="24" font-size="13" font-weight="600">heap</text><g><rect class="box" x="20" y="44" width="230" height="44" rx="8"/><text class="ink" x="34" y="71" font-size="14" font-weight="600">list</text><text class="dim" x="110" y="71" font-size="12.5">Cons(1, Box)</text></g><g><rect class="box" x="390" y="44" width="220" height="44" rx="8"/><text class="ink" x="404" y="71" font-size="14">Cons(2, Box)</text></g><g><rect class="box" x="390" y="102" width="220" height="44" rx="8"/><text class="ink" x="404" y="129" font-size="14">Nil</text></g><path class="curve" d="M250 66 C320 66 320 66 382 66"/><polygon class="dot" points="390,66 380,61 380,71"/></svg><figcaption>Each node holds a value and the next node's address: the size is fixed.</figcaption></figure>

`Nil` is the list's end. `use List::{Cons, Nil};` is for writing the variants shortly.

Let us measure the sizes:

```rust
#[derive(Debug)]
enum List {
    Cons(i32, Box<List>),
    Nil,
}

use List::{Cons, Nil};

use std::mem::size_of;

fn main() {
    println!("{}", size_of::<Box<i32>>());
    println!("{}", size_of::<Box<[i32; 1000]>>());
    println!("{}", size_of::<[i32; 1000]>());
    println!("{}", size_of::<List>());
}
```

```text
8
8
4000
16
```

## Deref: the * operator

Why does `Box` act like a reference? Thanks to the `Deref` trait. `*x` really means `*(x.deref())`:

```rust
use std::ops::Deref;

struct MyBox<T>(T);

impl<T> Deref for MyBox<T> {
    type Target = T;

    fn deref(&self) -> &T {
        &self.0
    }
}

fn main() {
    let x = MyBox(5);
    println!("{}", *x);
    println!("{}", *x.deref());
}
```

```text
5
5
```

`deref` returns `&T`. When written for your own type, `*` works on it too.

## Automatic conversion

Rust chains `deref` itself when needed. That is why `&String` passes where `&str` is wanted:

```rust
use std::ops::Deref;

struct MyBox<T>(T);

impl<T> Deref for MyBox<T> {
    type Target = T;

    fn deref(&self) -> &T {
        &self.0
    }
}

fn greet(name: &str) {
    println!("Hello, {name}");
}

fn main() {
    let name = MyBox(String::from("Ada"));
    greet(&name);
    greet(&name.0);
    println!("{}", name.len());
}
```

```text
Hello, Ada
Hello, Ada
3
```

`&MyBox<String>` → `&String` → `&str`. This **deref coercion** costs nothing at run time; it is resolved at compile time. The mutable version is `DerefMut`.

## Drop: cleanup

The `Drop` trait says "run this when this value is deleted". Closing a file and releasing a lock all live here:

```rust
struct Loud {
    name: &'static str,
}

impl Drop for Loud {
    fn drop(&mut self) {
        println!("dropping {}", self.name);
    }
}

fn main() {
    let _a = Loud { name: "a" };
    let _b = Loud { name: "b" };
    {
        let _inner = Loud { name: "inner" };
        println!("block ends");
    }
    println!("main ends");
}
```

```text
block ends
dropping inner
main ends
dropping b
dropping a
```

**The deletion order is the reverse of definition**: the last defined goes first. Struct fields, however, go in the order they are written.

This pattern is called RAII: a value holds the resource, and when the value goes the resource goes. There is no `finally` and no worry of "I forgot to close".

## Deleting early

`x.drop()` cannot be called directly, because it would be deleted a second time at the end:

```rust
struct Loud {
    name: &'static str,
}

impl Drop for Loud {
    fn drop(&mut self) {
        println!("dropping {}", self.name);
    }
}

fn main() {
    let a = Loud { name: "a" };
    a.drop();
}
```

```text
error[E0040]: explicit use of destructor method
  --> main.rs:13:7
   |
13 |     a.drop();
   |       ^^^^ explicit destructor calls not allowed
   |
help: consider using `drop` function
   |
13 -     a.drop();
13 +     drop(a);
   |
```

The right way is `std::mem::drop(x)` (it comes automatically, `drop(x)`). It is very simple: it takes ownership, does nothing, and its scope ends:

```rust
struct Loud {
    name: &'static str,
}

impl Drop for Loud {
    fn drop(&mut self) {
        println!("dropping {}", self.name);
    }
}

fn main() {
    let a = Loud { name: "a" };
    drop(a);
    println!("after drop");
}
```

```text
dropping a
after drop
```

## Summary

- `Box::new(x)` puts a value on the heap, and the address has a fixed size.
- A recursive type wants `Box` (`E0072`). Large data and trait objects are other uses.
- `Deref` provides `*`. Deref coercion turns `&String` into `&str`, at no cost.
- `Drop` writes cleanup. The order is the reverse of definition. RAII: a resource tied to a value.
- To delete early, `drop(x)`; `x.drop()` is forbidden (`E0040`).
