# Functions and Expressions

Rather than writing the same work again and again, we give it a name and call it by name. A named piece of
work is a **function**. So far we have only written `main`; now we write our own.

## Defining a function

```rust
fn main() {
    say_hello();
    say_hello();
}

fn say_hello() {
    println!("Hello!");
}
```

```text
Hello!
Hello!
```

It is defined with `fn` and **called** with `()` after its name. In Rust the order of definitions does not
matter: `say_hello` is written below `main` here and can still be called.

## Parameters

To give a function values from outside we write **parameters**. In Rust the type of every parameter is
**required**; the compiler does not infer it:

```rust
fn introduce(name: &str, age: i32) {
    println!("{name} is {age}");
}

fn main() {
    introduce("Ada", 36);
}
```

```text
Ada is 36
```

`name: &str` means "called name, of text type". `&str` is a text type; we will see what it means after ownership.
The values we give when calling, `"Ada"` and `36`, are called **arguments**.

Requiring types on parameters is no accident: a function's signature (name, parameters, return type) is a contract
for whoever uses it. The compiler can check a call without looking inside the function.

## Returning a value

For a function to give back its result we write the return type with `->`:

```rust
fn add(a: i32, b: i32) -> i32 {
    a + b
}

fn main() {
    let total = add(2, 3);
    println!("{total}");
}
```

```text
5
```

Note: there is **no semicolon** at the end of the `a + b` line. This is one of Rust's most important habits, because
Rust has two kinds of code.

## Statement and expression

- An **expression** produces a value: `5`, `a + b`, `square(3)`.
- A **statement** does some work and produces no value: `let x = 5;`.

Putting a semicolon after an expression turns it into a statement and its value is discarded. If the final line of a
function is an expression with no semicolon, its value is the return value. Add a semicolon and you get an error:

```rust
fn square(n: i32) -> i32 {
    n * n;
}

fn main() {
    println!("{}", square(3));
}
```

```text
error[E0308]: mismatched types
 --> main.rs:1:22
  |
1 | fn square(n: i32) -> i32 {
  |    ------            ^^^ expected `i32`, found `()`
  |    |
  |    implicitly returns `()` as its body has no tail or `return` expression
2 |     n * n;
  |          - help: remove this semicolon to return this value
```

The compiler says exactly this: the function promised an `i32`, but its body gave nothing, and the `help:` line suggests
removing the semicolon. You will see this error often. When you do, the first place to look is the end of the last line.

## Blocks are expressions too

Every block in curly braces is an expression and gives the value of its last line:

```rust
fn main() {
    let area = {
        let width = 4;
        let height = 5;
        width * height
    };
    println!("{area}");
}
```

```text
20
```

`if` is an expression too; we will use that in the next section.

## Returning early with return

To leave before the last line, write `return`:

```rust
fn safe_half(n: i32) -> i32 {
    if n < 0 {
        return 0;
    }
    n / 2
}

fn main() {
    println!("{}", safe_half(10));
    println!("{}", safe_half(-4));
}
```

```text
5
0
```

`if` tests a condition; when `n` is below zero the part in braces runs. The details are in the next section. `return` can be used anywhere, but the Rust habit is: at the end just write the value, and keep `return` for **early exits**.

## Functions that return no value

Without `->` a function returns unit (`()`), meaning no meaningful value. `main` is like this too. To print unit you need `{:?}`:

```rust
fn greet() {
    println!("hi");
}

fn main() {
    let nothing = greet();
    println!("{:?}", nothing);
}
```

```text
hi
()
```

## Returning several values

A tuple suits this job very well:

```rust
fn min_max(a: i32, b: i32) -> (i32, i32) {
    (a.min(b), a.max(b))
}

fn main() {
    let (low, high) = min_max(9, 4);
    println!("{low} {high}");
}
```

```text
4 9
```

The `let (low, high) = ...` line opens the returned tuple into two variables.

## Comments

`//` leaves a note in the code. Three slashes `///` make a documentation comment: it describes the item directly below it,
and the `cargo doc` command (Cargo comes later) produces a documentation page from them.

```rust
/// Returns the area of a rectangle.
fn area(width: u32, height: u32) -> u32 {
    // Width and height are never negative, so u32 is enough.
    width * height
}

fn main() {
    println!("{}", area(3, 4));
}
```

```text
12
```

A comment should say not "what it does" but, when the code cannot explain itself, "why it does it that way".

## Summary

- `fn name(parameter: type) -> return_type { ... }`. Parameter types are required.
- The expression with no semicolon on the last line is the return value. A semicolon there gives error `E0308`.
- Expressions produce values, statements do not. Blocks are expressions too.
- `return` is for early exits.
- Several values are returned with a tuple.
