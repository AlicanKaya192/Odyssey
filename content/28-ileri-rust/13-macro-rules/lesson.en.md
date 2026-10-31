# Declarative Macros

We have written `println!` and `vec!` since the first day. The `!` at the end says they are not functions but **macros**. In this section we write our own.

A function is called at runtime; the number and types of its arguments are fixed. A macro **produces code at compile time**: the compiler opens the macro in place, then compiles the resulting code normally. That is how `println!("{} {}", a, b)` and `vec![1, 2, 3]` take varying numbers of arguments.

Rust has two kinds of macro. The **declarative** kind in this section is written with `macro_rules!`; the procedural kind in the next section is a separate compiler plugin.

## The first macro

```rust
macro_rules! say_hello {
    () => {
        println!("hello");
    };
}

fn main() {
    say_hello!();
    say_hello!();
}
```

```text
hello
hello
```

Its shape resembles `match`: `(pattern) => { template };`. The pattern is empty, and the template is a `println!`.

## Capturing arguments

In a pattern, `$name:kind` captures a piece. The kind here is not a Rust type but **a kind of syntax piece**. `expr` means "an expression":

```rust
macro_rules! square {
    ($x:expr) => {
        $x * $x
    };
}

fn main() {
    println!("{}", square!(3));
    println!("{}", square!(1 + 2));
}
```

```text
9
9
```

Note the second line: C's text macros would make it `1 + 2 * 1 + 2` and give 5. In Rust, `$x` is placed as a whole, and the result is 9.

But there is another trap. `$x` appears twice in the template, so the expression **runs twice**:

```rust
macro_rules! square {
    ($x:expr) => {
        $x * $x
    };
}

fn next(counter: &mut u32) -> u32 {
    *counter += 1;
    *counter
}

fn main() {
    let mut counter = 0;
    println!("result {}", square!(next(&mut counter)));
    println!("calls {counter}");
}
```

```text
result 2
calls 2
```

The result was `1 * 2`. The cure is to take the value once and keep it. Note that the template is now inside double braces. The outer pair is the macro's boundary, the inner pair is Rust's block expression:

```rust
macro_rules! square {
    ($x:expr) => {{
        let value = $x;
        value * value
    }};
}

fn next(counter: &mut u32) -> u32 {
    *counter += 1;
    *counter
}

fn main() {
    let mut counter = 0;
    println!("result {}", square!(next(&mut counter)));
    println!("calls {counter}");
}
```

```text
result 1
calls 1
```

## Hygiene

Does `temp` inside the macro mix with the `temp` outside?

```rust
macro_rules! add_ten {
    ($x:expr) => {{
        let temp = 10;
        $x + temp
    }};
}

fn main() {
    let temp = 1;
    println!("{}", add_ten!(temp));
    println!("{temp}");
}
```

```text
11
1
```

It did not. Names the macro itself writes live in a separate context; this is called **hygiene**. The `temp` arriving as `$x` is the caller's `temp`. The result is `1 + 10`.

The same rule works in the other direction. You cannot see a variable the macro defines from outside:

```rust
macro_rules! define {
    () => {
        let value = 1;
    };
}

fn main() {
    define!();
    println!("{value}");
}
```

```text
error[E0425]: cannot find value `value` in this scope
 --> main.rs:9:16
  |
9 |     println!("{value}");
  |                ^^^^^ not found in this scope
  |
help: an identifier with the same name is defined here, but is not accessible due to
macro hygiene
 --> main.rs:3:13
  |
3 |         let value = 1;
  |             ^^^^^
...
8 |     define!();
  |     --------- in this macro invocation
  = note: this error originates in the macro `define` (in Nightly builds, run with -Z
    macro-backtrace for more info)
```

If you want it visible outside, the caller must give the name. `ident` captures a name:

```rust
macro_rules! define {
    ($name:ident, $value:expr) => {
        let $name = $value;
    };
}

fn main() {
    define!(answer, 42);
    println!("{answer}");
}
```

```text
42
```

## Repetition

The way to take varying numbers of arguments, like `vec!`, is the repetition pattern:

```rust
macro_rules! my_vec {
    ( $( $x:expr ),* $(,)? ) => {{
        let mut out = Vec::new();
        $( out.push($x); )*
        out
    }};
}

fn main() {
    println!("{:?}", my_vec![1, 2, 3]);
    println!("{:?}", my_vec!["a", "b",]);
    let empty: Vec<u32> = my_vec![];
    println!("{:?}", empty);
}
```

```text
[1, 2, 3]
["a", "b"]
[]
```

`$( $x:expr ),*` says: "zero or more of what is inside, with commas between." `$( out.push($x); )*` in the template produces a line for each captured item. This is not a loop: `my_vec![1, 2, 3]` turns into three separate `push` lines at compile time.

| Mark | Meaning |
|---|---|
| `*` | Zero or more |
| `+` | One or more |
| `?` | Zero or one |

So `$(,)?` means "an optional comma at the end".

## Several arms

Arms are tried from top to bottom like `match`, and the first match wins:

```rust
macro_rules! greet {
    () => {
        String::from("hello")
    };
    ($name:expr) => {
        format!("hello {}", $name)
    };
    ($name:expr, $times:literal) => {
        format!("hello {} x{}", $name, $times)
    };
}

fn main() {
    println!("{}", greet!());
    println!("{}", greet!("ada"));
    println!("{}", greet!("ada", 3));
}
```

```text
hello
hello ada
hello ada x3
```

If none matches, compilation stops:

```rust
macro_rules! square {
    ($x:expr) => {
        $x * $x
    };
}

fn main() {
    println!("{}", square!(1, 2));
}
```

```text
error: no rules expected `,`
 --> main.rs:8:29
  |
1 | macro_rules! square {
  | ------------------- when calling this macro
...
8 |     println!("{}", square!(1, 2));
  |                             ^ no rules expected this token in macro call
  |
note: while trying to match meta-variable `$x:expr`
 --> main.rs:2:6
  |
2 |     ($x:expr) => {
  |      ^^^^^^^
```

## Recursion

A macro can call itself. "Take the first, apply yourself to the rest" is a common pattern:

```rust
macro_rules! total {
    ($x:expr) => {
        $x
    };
    ($x:expr, $($rest:expr),+) => {
        $x + total!($($rest),+)
    };
}

fn main() {
    println!("{}", total!(5));
    println!("{}", total!(1, 2, 3, 4));
}
```

```text
5
10
```

`tt` (token tree) is the most flexible piece: one token, or an entire bracketed group. Counting tokens is done with it:

```rust
macro_rules! count {
    () => { 0usize };
    ($head:tt $($tail:tt)*) => { 1usize + count!($($tail)*) };
}

fn main() {
    println!("{}", count!());
    println!("{}", count!(a b c));
    println!("{}", count!(1 + (2 * 3)));
}
```

```text
0
3
3
```

`(2 * 3)` counted as one `tt`, and the result is 3: `1`, `+`, and the bracketed group.

## The real use: repeated code

A macro is most valuable for writing nearly the same `impl` for many types. The standard library produces much of its number code this way too:

```rust
trait TypeName {
    fn type_name() -> &'static str;
}

macro_rules! impl_type_name {
    ($($t:ty),* $(,)?) => {
        $(
            impl TypeName for $t {
                fn type_name() -> &'static str {
                    stringify!($t)
                }
            }
        )*
    };
}

impl_type_name!(i32, f64, Vec<u8>);

fn main() {
    println!("{}", i32::type_name());
    println!("{}", <Vec<u8>>::type_name());
}
```

```text
i32
Vec<u8>
```

`ty` captures a type. `stringify!` turns tokens into text without running them. It helps when writing our own `assert` too:

```rust
macro_rules! show {
    ($x:expr) => {
        println!("{} = {:?}", stringify!($x), $x)
    };
}

fn main() {
    let items = [1, 2, 3];
    show!(1 + 2);
    show!(items.len() * 2);
    println!("{}:{}", file!().ends_with(".rs"), line!() > 0);
}
```

```text
1 + 2 = 3
items.len() * 2 = 6
true:true
```

## Order and visibility

Unlike functions, macros depend on **text order**: definition first, then use.

```rust
fn main() {
    say_hello!();
}

macro_rules! say_hello {
    () => {
        println!("hello");
    };
}
```

```text
error: cannot find macro `say_hello` in this scope
 --> main.rs:2:5
  |
2 |     say_hello!();
  |     ^^^^^^^^^ consider moving the definition of `say_hello` before this call
  |
note: a macro with the same name exists, but it appears later
 --> main.rs:5:14
  |
5 | macro_rules! say_hello {
  |              ^^^^^^^^^

warning: unused macro definition: `say_hello`
 --> main.rs:5:14
  |
5 | macro_rules! say_hello {
  |              ^^^^^^^^^
  |
  = note: `#[warn(unused_macros)]` (part of `#[warn(unused)]`) on by default
```

To open one from a module, write `pub(crate) use`:

```rust
mod helpers {
    macro_rules! double {
        ($x:expr) => {
            $x * 2
        };
    }

    pub(crate) use double;
}

fn main() {
    println!("{}", helpers::double!(4));
}
```

```text
8
```

Opening it to other crates needs `#[macro_export]`. Paths inside the macro must then start with `$crate::`, otherwise they are looked up in the crate using the macro.

## Summary

- A macro produces code at compile time; `macro_rules!` consists of patterns and templates.
- `$x:expr` captures an expression and places it as a whole, but it runs again wherever it appears.
- Hygiene: a macro's own names do not mix with the caller's.
- `$( ... ),*` is repetition; in the template it produces code for each item.
- Arms are tried in order; a macro can call itself.
- Its best use is the same `impl` for many types. If a function is enough, write a function.
