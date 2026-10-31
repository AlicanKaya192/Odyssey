## Fragment kinds

| Kind | What it captures | Example |
|---|---|---|
| `expr` | Expression | `1 + 2`, `f(x)` |
| `ident` | Name | `value`, `Point` |
| `ty` | Type | `i32`, `Vec<u8>` |
| `tt` | One token or a bracketed group | `+`, `(a b)` |
| `pat` | Pattern | `Some(x)`, `1..=5` |
| `stmt` | Statement | `let a = 1` |
| `block` | Block | `{ a + 1 }` |
| `literal` | Literal value | `3`, `"text"` |
| `path` | Path | `std::mem::swap` |
| `item` | Item | `fn f() {}`, `struct S;` |
| `lifetime` | Lifetime | `'a` |
| `vis` | Visibility, may be empty | `pub`, `pub(crate)` |
| `meta` | Attribute contents | `derive(Debug)` |

## Repetition patterns

| Pattern | Matches |
|---|---|
| `$( $x:expr ),*` | `a, b, c` or nothing |
| `$( $x:expr ),+` | At least one |
| `$( $x:expr ),* $(,)?` | A trailing comma too |
| `$( $x:tt )*` | Space-separated tokens |
| `$( $k:expr => $v:expr ),*` | Pairs |

In the template a repetition must be at the same depth as in the pattern: if `$x` was captured inside a repetition, it is used inside `$( ... $x ... )*`.

## Common built-in macros

| Macro | What it gives |
|---|---|
| `stringify!(x)` | The text of the tokens |
| `concat!("a", 1)` | Joined constant text |
| `line!()`, `column!()`, `file!()` | The place in the source |
| `module_path!()` | The module path |
| `env!("NAME")` | An environment variable at compile time |
| `include_str!("path")` | Embeds a file as text |
| `compile_error!("message")` | Stops compilation with a message |
| `cfg!(windows)` | A configuration condition, a `bool` |

## Call forms

`m!()`, `m![]` and `m!{}` are all valid and go to the same arms. The habit: `()` for function-like ones, `[]` for list-like ones, `{}` or `()` with a final `;` for ones producing items.

## Module and crate

| Need | Written as |
|---|---|
| Same file, further down | Use it directly |
| By path within the crate | `pub(crate) use name;` |
| For other crates | `#[macro_export]` |
| Your own crate inside the macro | `$crate::path` |
