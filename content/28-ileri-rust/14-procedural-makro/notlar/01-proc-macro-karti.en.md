## Three kinds

| Kind | Attribute | Signature | Call |
|---|---|---|---|
| Function-like | `#[proc_macro]` | `fn(TokenStream) -> TokenStream` | `name!(...)` |
| Derive | `#[proc_macro_derive(Name)]` | `fn(TokenStream) -> TokenStream` | `#[derive(Name)]` |
| Attribute | `#[proc_macro_attribute]` | `fn(TokenStream, TokenStream) -> TokenStream` | `#[name(...)]` |

## What does what?

| Kind | Input | Output |
|---|---|---|
| Function-like | Inside the brackets | Replaces the call |
| Derive | The whole struct | Added beside the struct |
| Attribute | Arguments + item | Replaces the item |

## proc_macro tools

| Name | Its job |
|---|---|
| `input.into_iter()` | The `TokenTree`s |
| `input.to_string()` | The text of the tokens |
| `input.is_empty()` | Is it empty? |
| `"code".parse::<TokenStream>()` | Tokens from text |
| `stream.extend(other)` | Adds at the end |
| `iter.collect::<TokenStream>()` | A stream from tokens |
| `group.delimiter()` | `Brace`, `Parenthesis`, `Bracket`, `None` |
| `group.stream()` | The inside of the group |
| `Group::new(delim, stream)` | A new group |
| `punct.as_char()` | The character |
| `punct.spacing()` | `Joint` or `Alone` |

## Setup

| File | Contents |
|---|---|
| Root `Cargo.toml` | `my_macros = { path = "my_macros" }` |
| `my_macros/Cargo.toml` | `proc-macro = true` under `[lib]` |
| `my_macros/src/lib.rs` | The macro functions, `pub` |
| `src/main.rs` | `use my_macros::name;` |

## While producing

| What you want to produce | Inside `format!` |
|---|---|
| `{` and `}` | `{{` and `}}` |
| Quoted text | `{name:?}` |
| A number literal | `{count}usize` |
| A list | `vec!{items:?}` (for `Vec<String>`) |

## A trap: only macros are exported

A proc macro crate cannot export anything but macros:

```rust
use proc_macro::TokenStream;

pub fn helper() {}

#[proc_macro]
pub fn answer(_input: TokenStream) -> TokenStream {
    "42".parse().unwrap()
}
```

```text
error: `proc-macro` crate types currently cannot export any items other than functions
tagged with `#[proc_macro]`, `#[proc_macro_derive]`, or `#[proc_macro_attribute]`
 --> my_macros/src/lib.rs:3:1
  |
3 | pub fn helper() {}
  | ^^^^^^^^^^^^^^^

error: could not compile `my_macros` (lib) due to 1 previous error
```

If you need a trait the derive implements, that trait lives in a separate crate; real libraries are pairs of crates for this reason (`serde` and `serde_derive`).
