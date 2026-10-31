## Double evaluation

An expression runs as many times as `$x` appears in the template. With a side effect (a counter, reading a file) the result is wrong, and an expensive expression does the work twice. If it appears more than once, start with `let value = $x;`.

## Double braces

If a template holds several statements and produces a value, `{{ ... }}` is needed: the outer pair is the macro's boundary, the inner pair is a block expression. With one pair, a template containing `let` does not compile where an expression is expected.

## What may follow an expression?

So that the end of an `expr` is known, only certain marks may follow it:

```rust
macro_rules! pair {
    ($a:expr $b:expr) => {
        ($a, $b)
    };
}

fn main() {
    let _ = pair!(1 2);
}
```

```text
error: `$a:expr` is followed by `$b:expr`, which is not allowed for `expr` fragments
 --> main.rs:2:14
  |
2 |     ($a:expr $b:expr) => {
  |              ^^^^^^^ not allowed after `expr` fragments
  |
  = note: allowed there are: `=>`, `,` or `;`
```

| Fragment | What may follow |
|---|---|
| `expr`, `stmt` | `=>`, `,`, `;` |
| `pat` | `=>`, `,`, `=`, `if`, `in` |
| `ty`, `path` | `=>`, `,`, `=`, `;`, `:`, `{`, `[`, `>`, `as`, `where` |
| `ident`, `tt`, `literal`, `block` | Anything |

## The recursion limit

A self-calling macro has a default limit of 128 steps. A `count!` over 200 tokens stops with `recursion limit reached`. The limit can be raised with `#![recursion_limit = "256"]`, but a macro processing many tokens slows compilation.

## What does hygiene not cover?

Hygiene is for local variables and labels. Function, type and module names in a template are looked up where it is called. That is why a macro opened with `#[macro_export]` writes `$crate::helper()`; `::std::...` serves the same purpose.

## Debugging

| Tool | What it does |
|---|---|
| `cargo expand` (installed separately) | Shows the opened code |
| `stringify!` | Prints the captured piece |
| `compile_error!` | Gives a message on an unexpected arm |

Error messages often show the inside of the macro, so keeping patterns small and growing them step by step helps.

## When not to write one?

| Need | Better tool |
|---|---|
| Work on one type | A function |
| Many types, the same behaviour | Generics and traits |
| A constant calculation | `const fn` |
| Just writing less | A helper function |

Macros make code harder to read, autocomplete and diagnose. If a function or generics solve it, do not write a macro. Write one when you need varying numbers of arguments, new syntax, or to produce part of a type (a name, a field).
