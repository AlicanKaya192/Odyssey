# Modules and Visibility

As a program grows, one file is not enough. A **module** splits code into named parts and decides what is visible from outside. In Rust everything is **private** by default.

## mod and pub

```rust
mod shapes {
    pub fn area(w: u32, h: u32) -> u32 {
        w * h
    }

    pub fn perimeter(w: u32, h: u32) -> u32 {
        double(w + h)
    }

    fn double(n: u32) -> u32 {
        n * 2
    }
}

fn main() {
    println!("{}", shapes::area(3, 4));
    println!("{}", shapes::perimeter(3, 4));
}
```

```text
12
14
```

`mod` opens a module, and `::` goes inside. `pub` means "visible from outside".

If `pub` is forgotten:

```rust
mod shapes {
    fn area(w: u32, h: u32) -> u32 {
        w * h
    }
}

fn main() {
    println!("{}", shapes::area(3, 4));
}
```

```text
error[E0603]: function `area` is private
 --> main.rs:8:28
  |
8 |     println!("{}", shapes::area(3, 4));
  |                            ^^^^ private function
  |
note: the function `area` is defined here
 --> main.rs:2:5
  |
2 |     fn area(w: u32, h: u32) -> u32 {
  |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```

This limit is a feature: anything you did not mark `pub` can be changed without breaking anyone.

## use: a short name

Writing the full path each time gets long:

```rust
mod shapes {
    pub mod circle {
        pub fn area_times_100(r: u32) -> u32 {
            314 * r * r
        }
    }
}

use shapes::circle;

fn main() {
    println!("{}", shapes::circle::area_times_100(2));
    println!("{}", circle::area_times_100(1));
}
```

```text
1256
314
```

`use` brings a name into the current scope. We were already writing it for the standard library: `use std::collections::HashMap;`. `as` renames, and braces take several at once:

```rust
use std::collections::{BTreeMap, HashMap};
use std::fmt::Result as FmtResult;
```

The custom is to bring the module for functions (`shapes::area`) and the thing itself for types and structs (`HashMap`): looking at a call shows where the function comes from.

## Paths: crate, self, super

| Written | Starts from |
|---|---|
| `crate::a::b` | The project's root |
| `self::b` | The module you are in |
| `super::b` | One module up |

```rust
fn top() -> &'static str {
    "top"
}

mod outer {
    pub fn name() -> &'static str {
        "outer"
    }

    pub mod inner {
        pub fn report() {
            println!("{}", super::name());
            println!("{}", self::own());
            println!("{}", crate::top());
        }

        fn own() -> &'static str {
            "inner"
        }
    }
}

fn main() {
    outer::inner::report();
}
```

```text
outer
inner
top
```

`use super::*;` in tests is exactly this: the test module takes in everything from its parent.

## Struct fields are hidden too

Writing `pub struct` does not open the fields. Each field needs its own `pub`:

```rust
mod people {
    pub struct Age {
        value: u8,
    }
}

fn main() {
    let age = people::Age { value: 200 };
    println!("{}", age.value);
}
```

```text
error[E0616]: field `value` of struct `Age` is private
 --> main.rs:9:24
  |
9 |     println!("{}", age.value);
  |                        ^^^^^ private field
```

The "validating constructor" idea of the previous section completes here. Since the field is hidden, an invalid value can only come through the constructor, which rejects it:

```rust
mod people {
    #[derive(Debug)]
    pub struct Age {
        value: u8,
    }

    impl Age {
        pub fn new(value: i32) -> Result<Age, String> {
            if value < 0 || value > 150 {
                return Err(format!("age must be 0-150, got {value}"));
            }
            Ok(Age { value: value as u8 })
        }

        pub fn get(&self) -> u8 {
            self.value
        }
    }
}

fn main() {
    let age = people::Age::new(36).expect("valid");
    println!("{}", age.get());
    println!("{:?}", people::Age::new(200));
}
```

```text
36
Err("age must be 0-150, got 200")
```

An enum differs: all variants of a `pub enum` are open.

## Module files

`mod lib_name;` (with a semicolon) means "this module's content is in another file":

```text
src/
├── main.rs        mod shapes;
└── shapes.rs      pub fn area(...)
```

Sub-modules live in a folder:

```text
src/
├── main.rs        mod shapes;
├── shapes.rs      pub mod circle;
└── shapes/
    └── circle.rs  pub fn area(...)
```

In older projects you see `shapes/mod.rs`, which does the same job. Inside the file you do **not** write `mod shapes { ... }`; the file itself is the module.

A working example:

```rust
mod shapes;

fn main() {
    println!("{}", shapes::area(3, 4));
}
```

```text
12
```

The content of `shapes.rs`:

```rust
pub fn area(w: u32, h: u32) -> u32 {
    w * h
}

```

Rust does not find files by itself. A file with no `mod shapes;` line is not even compiled. This differs from the Python habit of "the file exists, so it is a module".

## Package, crate, module

| Concept | What |
|---|---|
| **Package** | A folder with a `Cargo.toml` |
| **Crate** | The unit the compiler compiles in one go |
| **Binary crate** | `src/main.rs`: a running program |
| **Library crate** | `src/lib.rs`: code for others to use |
| **Module** | A part inside a crate |

A package can hold both `main.rs` and `lib.rs`. A good layout is this: all the logic in `lib.rs`, and `main.rs` only reads and calls. So the logic stays testable.

```rust
// src/lib.rs
pub fn greet(name: &str) -> String {
    format!("Hello, {name}!")
}
```

```rust
// src/main.rs (if the package is named hello)
fn main() {
    println!("{}", hello::greet("Ada"));
}
```

## Degrees of pub

| Written | Who sees it |
|---|---|
| (nothing) | This module and those below |
| `pub(super)` | One module up |
| `pub(crate)` | The whole crate |
| `pub` | Everyone |

Open a thing only as much as needed: once `pub` is written and someone starts using it, taking it back gets hard.

## pub use: opening again

The inner layout and the face shown outside can differ:

```rust
mod geometry {
    mod circle {
        pub fn area_times_100(r: u32) -> u32 {
            314 * r * r
        }
    }

    pub use circle::area_times_100;
}

fn main() {
    println!("{}", geometry::area_times_100(2));
}
```

```text
1256
```

The user writes `geometry::area` rather than `geometry::circle::area`. Even if you change the inner folder layout, their code does not break.

## Summary

- `mod` opens a module, `::` goes inside; everything is private by default.
- `pub` opens. In a struct each field needs its own `pub`; enum variants are open by themselves.
- `use` brings a short name. `crate::`, `self::`, `super::` are path starts.
- `mod x;` takes its content from `x.rs`; files are not found by themselves.
- `main.rs` is a binary crate, `lib.rs` a library crate. Put the logic in the library.
- `pub use` shows a face independent of the inner layout.
