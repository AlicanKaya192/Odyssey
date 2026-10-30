# Variables and Mutability

While running, a program needs to remember values: a price, a name, a total. Giving a value a name
and using it through that name later is called a **variable**.

## Variables with let

```rust
fn main() {
    let age = 36;
    let city = "Istanbul";
    println!("{} lives in {}", age, city);
    println!("{age} lives in {city}");
}
```

```text
36 lives in Istanbul
36 lives in Istanbul
```

`let` says "I am defining a name". The value on the right of `=` is bound to the name on the left.
You can use a variable inside text in two ways:

- `{}` followed by the value after a comma: `println!("{}", age)`
- The name directly inside the braces: `println!("{age}")`

The second form is shorter and easier to read, but it takes only a plain variable name. You cannot
write an operation such as `{age + 1}`; for that, use the first form.

Variable names use lowercase and underscores: `total_price`. Rust calls this `snake_case` and warns
if you write it differently.

## Variables do not change by default

Here is the first Rust surprise. In most languages a variable's value can be changed whenever you
like. In Rust it cannot:

```rust
fn main() {
    let x = 5;
    println!("{x}");
    x = 6;
    println!("{x}");
}
```

```text
error[E0384]: cannot assign twice to immutable variable `x`
 --> main.rs:4:5
  |
2 |     let x = 5;
  |         - first assignment to `x`
3 |     println!("{x}");
4 |     x = 6;
  |     ^^^^^ cannot assign twice to immutable variable
  |
help: consider making this binding mutable
  |
2 |     let mut x = 5;
  |         +++
```

The compiler states the problem and gives the fix on the `help:` line. This looks like a restriction
but it is a big gain: if a variable has no `mut` mark, **you are sure it never changes anywhere**. When
reading a long function that saves you a lot of thinking.

## Changeable variables with mut

If the value really needs to change, you say so explicitly:

```rust
fn main() {
    let mut score = 10;
    println!("start: {score}");
    score += 5;
    println!("after: {score}");
}
```

```text
start: 10
after: 15
```

`mut` comes from "mutable", meaning changeable. `+=` adds to the value on the left:
`score += 5` does the same as `score = score + 5`.

If you write `mut` needlessly on a variable that never changes, the compiler warns. The rule is simple:
**write it without `mut` first, add it if the compiler asks.**

## Shadowing a variable

You can write `let` again with the same name. This is called **shadowing**: the new variable covers the old one.

```rust
fn main() {
    let price = 100;
    let price = price + 20;
    let price = price * 2;
    println!("{price}");
}
```

```text
240
```

At first glance it looks the same as `mut`, but there are two important differences:

<figure class="fig"><div class="versus"><div><h4>mut</h4>The same variable's value changes. The type must stay the same.</div><div><h4>Shadowing</h4>A brand new variable opens. The old value still exists but can no longer be reached by that name. The type can change too.</div></div><figcaption>Shadow when you transform a value and continue under the same name; use <code>mut</code> when you update the same thing.</figcaption></figure>

Being able to change the type is very useful in practice. You need not invent two names to turn a
text into its length:

```rust
fn main() {
    let text = "hello";
    let text = text.len();
    println!("{text}");
}
```

```text
5
```

`.len()` gives the length of the text. If you try the same with `mut` you get an error, because you are
trying to change the type:

```rust
fn main() {
    let mut text = "hello";
    text = text.len();
    println!("{text}");
}
```

```text
error[E0308]: mismatched types
 --> main.rs:3:12
  |
2 |     let mut text = "hello";
  |                    ------- expected due to this value
3 |     text = text.len();
  |            ^^^^^^^^^^ expected `&str`, found `usize`
```

`E0308` means "the types do not match" and is one of the most common errors you will see in Rust:
`expected` shows the type wanted, `found` shows what you gave.

## Scope: where does a variable live?

Curly braces open a **block**. A variable defined inside a block ceases to exist when the block ends:

```rust
fn main() {
    let x = 1;
    {
        let x = 2;
        println!("inner: {x}");
    }
    println!("outer: {x}");
}
```

```text
inner: 2
outer: 1
```

The `x` inside the block shadows the outer one only for the length of the block. When the block ends the
outer one is visible again. This idea of scope will be the basis of ownership later.

## Constants: const

For a value that will never change and is valid throughout the program, use `const`:

```rust
const MAX_POINTS: u32 = 100_000;

fn main() {
    println!("{MAX_POINTS}");
}
```

```text
100000
```

How it differs from `let`:

| | `let` | `const` |
|---|---|---|
| Writing the type | Optional | **Required** |
| When the value is known | May be while running | Must be known while compiling |
| Can it be `mut` | Yes | No |
| Where it is written | Inside a function | Anywhere, also at the top of a file |
| Name style | `snake_case` | `UPPER_CASE` |

The `u32` here is a **type**: an unsigned (cannot be negative) 32-bit whole number. We will see types in the
next section. The `_` in a number only makes reading easier: `100_000` and `100000` are the same.

## Unused variables

The compiler warns about a variable you define and never use. If it is unused on purpose, put `_` in front
of the name and the warning goes away: `let _unused = 5;`

## Summary

- `let` defines a name. Variables **do not change** by default; for change, use `let mut`.
- With `{age}` you can write a variable name directly into text.
- Writing `let` again with the same name is shadowing: it is a new variable and its type may change.
- When a block ends, the variables inside it cease to exist.
- `const` is an unchanging value known at compile time, with its type written.
