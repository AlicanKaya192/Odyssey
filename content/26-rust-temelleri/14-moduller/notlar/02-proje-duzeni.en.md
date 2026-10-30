## A typical layout

```text
my_tool/
├── Cargo.toml
├── src/
│   ├── main.rs      Reads arguments, calls lib, writes errors
│   ├── lib.rs       The face opened outwards
│   ├── parser.rs    One job
│   └── report.rs    Another job
└── tests/
    └── cli.rs       Integration tests
```

Each file in the `tests/` folder compiles as a separate crate and, like someone using the library from outside, sees only what is `pub`.

## How to split a module?

| Measure | Example |
|---|---|
| Code that changes together stays together | A parser and its error type |
| By responsibility, not by kind | `parser`, `report`; not `structs`, `functions` |
| Small face, large inside | Few `pub`, much hidden |

Start in one file. Split when the file becomes hard to read; do not build a folder tree up front.

## Direction of dependency

`main.rs` → `lib.rs` → modules. If two modules use each other, consider moving the shared part to a third module. Rust allows this, but it makes reading harder.

## What to avoid

- `use a::*;`: it is not clear where a name comes from. The exception: `use super::*;` in tests.
- Writing `pub` on everything: it cancels the benefit of privacy.
- Very deep paths: `a::b::c::d::e`. Flatten with `pub use`.
