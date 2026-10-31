# Procedural Macros

When you write `#[derive(Debug)]`, the compiler looks at the struct's fields and produces code. `macro_rules!` cannot do this: it puts matching pieces in place, but it cannot inspect "how many fields, what names?" with arbitrary code. That is what a **procedural macro** is for.

A procedural macro is an ordinary Rust function that runs at compile time. It takes tokens and gives tokens. You write whatever code you like in between.

## A separate crate

Since the compiler will **run** the macro's code, it has to compile it first and load it into itself. That is why procedural macros live in their own crate. The root package:

```toml
[package]
name = "app"
version = "0.1.0"
edition = "2024"

[dependencies]
my_macros = { path = "my_macros" }
```

`my_macros/Cargo.toml`:

```toml
[package]
name = "my_macros"
version = "0.1.0"
edition = "2024"

[lib]
proc-macro = true
```

`proc-macro = true` sets this crate's type.

## The first macro

There are three kinds of procedural macro. The simplest is function-like. `my_macros/src/lib.rs`:

```rust
use proc_macro::TokenStream;

#[proc_macro]
pub fn answer(_input: TokenStream) -> TokenStream {
    "42".parse().unwrap()
}
```

`src/main.rs`:

```rust
use my_macros::answer;

fn main() {
    println!("{}", answer!());
}
```

```text
42
```

The `proc_macro` crate comes with the compiler and is not downloaded. Turning text into tokens with `parse` is the easiest way to produce code.

## TokenStream

The input is not text but a sequence of tokens. Each is one of four kinds:

```rust
use proc_macro::{TokenStream, TokenTree};

#[proc_macro]
pub fn token_kinds(input: TokenStream) -> TokenStream {
    let kinds: Vec<&str> = input
        .into_iter()
        .map(|token| match token {
            TokenTree::Ident(_) => "ident",
            TokenTree::Punct(_) => "punct",
            TokenTree::Literal(_) => "literal",
            TokenTree::Group(_) => "group",
        })
        .collect();
    format!("{:?}", kinds.join(" ")).parse().unwrap()
}
```

```rust
use my_macros::token_kinds;

fn main() {
    println!("{}", token_kinds!(total + 1 * (a - b)));
}
```

```text
ident punct literal punct group
```

| Kind | Example |
|---|---|
| `Ident` | `total`, `struct` |
| `Punct` | `+`, `:` (one character) |
| `Literal` | `1`, `"text"` |
| `Group` | `(a - b)` as a whole; its inside is `group.stream()` |

Note: this is not a syntax tree. The macro does not know whether `total` is defined, nor the precedence of `1 * (a - b)`; it only sees tokens in order. `total` is not defined anywhere and compilation still passed, because the macro ate it.

## No hygiene

In the `macro_rules!` section a variable the macro defined was not visible outside. In code produced with `parse`, it is:

```rust
use proc_macro::TokenStream;

#[proc_macro]
pub fn make_x(_input: TokenStream) -> TokenStream {
    "let x = 1;".parse().unwrap()
}
```

```rust
use my_macros::make_x;

fn main() {
    make_x!();
    println!("{x}");
}
```

```text
1
```

Produced names live in the same place as the caller's. So accidentally shadowing the caller's variable is up to you. Give helper variables rare names (like `__macro_temp`).

## derive

A `derive` macro takes the struct's tokens and adds code **beside** it; it does not change the struct itself. Let us write our own `FieldNames`, listing the field names.

```rust
use proc_macro::{Delimiter, Spacing, TokenStream, TokenTree};

#[proc_macro_derive(FieldNames)]
pub fn field_names(input: TokenStream) -> TokenStream {
    let tokens: Vec<TokenTree> = input.into_iter().collect();
    let name = struct_name(&tokens);
    let fields = field_list(&tokens);
    format!(
        "impl {name} {{
            fn field_names() -> Vec<&'static str> {{
                vec!{fields:?}
            }}
        }}"
    )
    .parse()
    .unwrap()
}

fn struct_name(tokens: &[TokenTree]) -> String {
    let mut iter = tokens.iter();
    while let Some(token) = iter.next() {
        if token.to_string() == "struct" {
            return iter.next().unwrap().to_string();
        }
    }
    panic!("FieldNames works only on structs");
}

fn field_list(tokens: &[TokenTree]) -> Vec<String> {
    let body = tokens.iter().find_map(|token| match token {
        TokenTree::Group(group) if group.delimiter() == Delimiter::Brace => Some(group),
        _ => None,
    });
    let inner: Vec<TokenTree> = body.unwrap().stream().into_iter().collect();
    // A field name is an identifier directly before a single ':'.
    inner
        .windows(2)
        .filter_map(|pair| match pair {
            [TokenTree::Ident(name), TokenTree::Punct(mark)]
                if mark.as_char() == ':' && mark.spacing() == Spacing::Alone =>
            {
                Some(name.to_string())
            }
            _ => None,
        })
        .collect()
}
```

```rust
use my_macros::FieldNames;

#[derive(FieldNames)]
struct Point {
    x: i32,
    y: i32,
    label: std::string::String,
}

fn main() {
    println!("{:?}", Point::field_names());
    let point = Point { x: 1, y: 2, label: String::new() };
    println!("{} {} {:?}", point.x, point.y, point.label);
}
```

```text
["x", "y", "label"]
1 2 ""
```

The parsing is in our hands:

- `struct_name`: the name is the token after the word `struct`.
- `field_list`: inside the brace group, the name right before a single `:`.
- `Spacing::Alone`: `::` arrives as two separate `Punct`s, and the first has `Joint` spacing. Without this, `std` in `std::string::String` would look like a field.

Inside `format!`, braces of the code to produce are written `{{` and `}}`.

This parser is enough for teaching but fragile: it still works for a field type like `HashMap<K, V>`, but `enum`s, tuple structs and fields with attributes need rewriting. We will discuss the real solution shortly.

## attribute

The third kind **replaces** the item: the returned tokens take the place of the original. It has two inputs, the arguments and the item itself:

```rust
use proc_macro::{Delimiter, Group, TokenStream, TokenTree};

#[proc_macro_attribute]
pub fn logged(_args: TokenStream, item: TokenStream) -> TokenStream {
    let mut tokens: Vec<TokenTree> = item.into_iter().collect();

    let mut iter = tokens.iter();
    let mut name = String::new();
    while let Some(token) = iter.next() {
        if token.to_string() == "fn" {
            name = iter.next().unwrap().to_string();
            break;
        }
    }

    let Some(TokenTree::Group(body)) = tokens.pop() else {
        panic!("logged works only on functions");
    };
    let mut new_body: TokenStream =
        format!("println!(\"enter {name}\");").parse().unwrap();
    new_body.extend(body.stream());
    tokens.push(TokenTree::Group(Group::new(Delimiter::Brace, new_body)));
    tokens.into_iter().collect()
}
```

```rust
use my_macros::logged;

#[logged]
fn add(a: i32, b: i32) -> i32 {
    a + b
}

fn main() {
    println!("{}", add(2, 3));
}
```

```text
enter add
5
```

The last token is the brace group that is the function's body. We took it out, added a `println!` at its start, built a new `Group`, and put it back. Had we not put it back, the function would have no body: in an attribute macro, what you give back is the code.

## Reporting errors

A panic in a macro becomes a compile error:

```rust
use my_macros::FieldNames;

#[derive(FieldNames)]
enum Color {
    Red,
}

fn main() {
    let _ = Color::Red;
}
```

```text
error: proc-macro derive panicked
 --> src/main.rs:3:10
  |
3 | #[derive(FieldNames)]
  |          ^^^^^^^^^^
  |
  = help: message: FieldNames works only on structs

error: could not compile `app` (bin "app") due to 1 previous error
```

It works, but says "the macro blew up". Neater is to produce `compile_error!`:

```rust
use proc_macro::TokenStream;

#[proc_macro]
pub fn only_empty(input: TokenStream) -> TokenStream {
    if input.is_empty() {
        return "0".parse().unwrap();
    }
    "compile_error!(\"only_empty takes no arguments\")".parse().unwrap()
}
```

```rust
use my_macros::only_empty;

fn main() {
    println!("{}", only_empty!(1));
}
```

```text
error: only_empty takes no arguments
 --> src/main.rs:4:20
  |
4 |     println!("{}", only_empty!(1));
  |                    ^^^^^^^^^^^^^^
  |
  = note: this error originates in the macro `only_empty` (in Nightly builds, run with
    -Z macro-backtrace for more info)

error: could not compile `app` (bin "app") due to 1 previous error
```

## Summary

- A procedural macro: a function run at compile time, taking and giving a `TokenStream`.
- It needs a separate crate and `proc-macro = true`.
- Three kinds: `#[proc_macro]`, `#[proc_macro_derive]`, `#[proc_macro_attribute]`.
- Tokens are of four kinds; this is not a syntax tree, and there is no type information.
- `derive` adds beside, an attribute replaces.
- For errors, produce `compile_error!`.
