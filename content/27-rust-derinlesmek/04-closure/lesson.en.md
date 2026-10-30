# Closures

You have seen the form `|x| x + 1` in several places. This is a **closure**: a nameless function written inline. It differs from an ordinary function in two ways: it is written shortly, and it **can use the variables around it.**

## Syntax

```rust
fn main() {
    let double = |x| x * 2;
    let add = |a: i32, b: i32| -> i32 { a + b };
    let hello = || println!("hello");
    println!("{}", double(4));
    println!("{}", add(2, 3));
    hello();
}
```

```text
8
5
hello
```

| Part | Meaning |
|---|---|
| <code>&#124;a, b&#124;</code> | Parameters, between vertical bars |
| What follows | The body; a single expression needs no braces |
| Types | Usually inferred, written if you wish |

A type once inferred is fixed. The same closure cannot be called with two different types:

```rust
fn main() {
    let same = |x| x;
    println!("{}", same(1));
    println!("{}", same("text"));
}
```

```text
error[E0308]: mismatched types
 --> main.rs:4:25
  |
4 |     println!("{}", same("text"));
  |                    ---- ^^^^^^ expected integer, found `&str`
  |                    |
  |                    arguments to this function are incorrect
  |
note: expected because the closure was earlier called with an argument of type
`{integer}`
 --> main.rs:3:25
  |
3 |     println!("{}", same(1));
  |                    ---- ^ expected because this argument is of type `{integer}`
  |                    |
  |                    in this closure call
note: closure parameter defined here
 --> main.rs:2:17
  |
2 |     let same = |x| x;
  |                 ^
```

## Capturing the surroundings

An ordinary function cannot see an outer local variable. A closure can:

```rust
fn main() {
    let offset = 10;
    let add = |x| x + offset;
    println!("{}", add(1));
    println!("{offset}");
}
```

```text
11
10
```

This is called **capturing**. The variable `add` captured `offset`.

## Three ways of capturing

The compiler looks at the body and picks the least permission needed:

```rust
fn main() {
    let name = String::from("Ada");
    let read = || println!("{name}");
    read();
    println!("{name}");

    let mut count = 0;
    let mut bump = || count += 1;
    bump();
    bump();
    println!("{count}");

    let text = String::from("gone");
    let consume = || drop(text);
    consume();
}
```

```text
Ada
Ada
2
```

| What the body does | Capture | Afterwards |
|---|---|---|
| Only reads | A `&` borrow | Readable outside too |
| Changes | A `&mut` borrow | The closure must be `mut` |
| Takes ownership | A move | Not usable outside |

The borrowing rules hold here too. While a closure holds a variable by `&mut`, you cannot read it from outside:

```rust
fn main() {
    let mut count = 0;
    let mut bump = || count += 1;
    println!("{count}");
    bump();
}
```

```text
error[E0502]: cannot borrow `count` as immutable because it is also borrowed as mutable
 --> main.rs:4:16
  |
3 |     let mut bump = || count += 1;
  |                    -- ----- first borrow occurs due to use of `count` in closure
  |                    |
  |                    mutable borrow occurs here
4 |     println!("{count}");
  |                ^^^^^ immutable borrow occurs here
5 |     bump();
  |     ---- mutable borrow later used here
```

## move

`move` moves ownership into the closure even when the body does not need it. It is needed if the closure will outlive local variables:

```rust
fn make_greeter() -> impl Fn() -> String {
    let name = String::from("Ada");
    || format!("Hello, {name}")
}

fn main() {
    println!("{}", make_greeter()());
}
```

```text
error[E0373]: closure may outlive the current function, but it borrows `name`, which is
owned by the current function
 --> main.rs:3:5
  |
3 |     || format!("Hello, {name}")
  |     ^^                  ---- `name` is borrowed here
  |     |
  |     may outlive borrowed value `name`
  |
note: closure is returned here
 --> main.rs:3:5
  |
3 |     || format!("Hello, {name}")
  |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^
help: to force the closure to take ownership of `name` (and any other referenced
variables), use the `move` keyword
  |
3 |     move || format!("Hello, {name}")
  |     ++++
```

```rust
fn make_greeter() -> impl Fn() -> String {
    let name = String::from("Ada");
    move || format!("Hello, {name}")
}

fn main() {
    let greet = make_greeter();
    println!("{}", greet());
}
```

```text
Hello, Ada
```

In section 10 we will write this all the time with threads. A `Copy` value is copied with `move`, and the original variable stays usable.

## Taking a closure as a parameter

Each closure has its own nameless type, so it is taken with generics. The bound is one of three traits:

| Trait | How many calls | What it can do |
|---|---|---|
| `FnOnce` | At least once | May consume what it captured |
| `FnMut` | Many times | May change what it captured |
| `Fn` | Many times, even at once | Only reads |

```rust
fn apply<F: Fn(i32) -> i32>(f: F, value: i32) -> i32 {
    f(f(value))
}

fn repeat<F: FnMut()>(mut f: F, times: u32) {
    for _ in 0..times {
        f();
    }
}

fn finish<F: FnOnce() -> String>(f: F) -> String {
    f()
}

fn main() {
    println!("{}", apply(|x| x + 3, 1));
    let mut total = 0;
    repeat(|| total += 2, 3);
    println!("{total}");
    let text = String::from("done");
    println!("{}", finish(|| text));
}
```

```text
7
6
done
```

An `Fn` is also an `FnMut` and an `FnOnce`. In a parameter, **ask for the loosest you can**: `FnOnce` if you call it once, `FnMut` if you call it many times and it may change things. So more closures are accepted.

A consuming closure cannot be called twice:

```rust
fn main() {
    let text = String::from("gone");
    let consume = || drop(text);
    consume();
    consume();
}
```

```text
error[E0382]: use of moved value: `consume`
 --> main.rs:5:5
  |
4 |     consume();
  |     --------- `consume` moved due to this call
5 |     consume();
  |     ^^^^^^^ value used here after move
  |
note: closure cannot be invoked more than once because it moves the variable `text` out
of its environment
 --> main.rs:3:27
  |
3 |     let consume = || drop(text);
  |                           ^^^^
note: this value implements `FnOnce`, which causes it to be moved when called
 --> main.rs:4:5
  |
4 |     consume();
  |     ^^^^^^^
```

## A function name works too

A function name can be given where a closure is expected:

```rust
fn double(n: i32) -> i32 {
    n * 2
}

fn apply(f: fn(i32) -> i32, value: i32) -> i32 {
    f(value)
}

fn main() {
    println!("{}", apply(double, 4));
    let values: Vec<i32> = vec![1, 2].into_iter().map(double).collect();
    println!("{:?}", values);
    let wrapped: Vec<Option<i32>> = vec![1, 2].into_iter().map(Some).collect();
    println!("{:?}", wrapped);
}
```

```text
8
[2, 4]
[Some(1), Some(2)]
```

`Some` and a tuple struct's constructor are functions too. The form `fn(i32) -> i32` is a **function pointer** type: it captures nothing.

## Returning a closure

Since the real type is nameless, `impl Fn` is returned. If it captures a local variable, `move` is required:

```rust
fn adder(n: i32) -> impl Fn(i32) -> i32 {
    move |x| x + n
}

fn main() {
    let add5 = adder(5);
    let add9 = adder(9);
    println!("{} {}", add5(1), add9(1));
}
```

```text
6 10
```

## Keeping one somewhere

It is held in a struct field with a generic:

```rust
struct Lazy<F: Fn() -> u32> {
    compute: F,
    value: Option<u32>,
}

impl<F: Fn() -> u32> Lazy<F> {
    fn new(compute: F) -> Self {
        Lazy { compute, value: None }
    }

    fn get(&mut self) -> u32 {
        if let Some(v) = self.value {
            return v;
        }
        println!("computing");
        let v = (self.compute)();
        self.value = Some(v);
        v
    }
}

fn main() {
    let mut lazy = Lazy::new(|| 6 * 7);
    println!("{}", lazy.get());
    println!("{}", lazy.get());
}
```

```text
computing
42
42
```

This is a **lazy** computation example: the function runs only once, when needed.

## Summary

- `|x| x + 1` is a nameless function; types are usually inferred and fixed once.
- It captures its surroundings: reading `&`, changing `&mut`, consuming a move. Borrow rules hold.
- `move` forces ownership over; it is needed if a closure outlives locals.
- `FnOnce`, `FnMut`, `Fn`: ask for the loosest in a parameter.
- A function name works too. When returning, `-> impl Fn(...)` and `move`.
