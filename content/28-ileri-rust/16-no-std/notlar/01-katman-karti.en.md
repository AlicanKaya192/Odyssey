## What is where?

| Name | Layer |
|---|---|
| `Option`, `Result` | `core` |
| Slices, `str` methods | `core` |
| `Iterator`, closures | `core` |
| `Cell`, `RefCell` | `core` |
| Atomics | `core` |
| `core::fmt::Write`, `write!` | `core` |
| `Vec`, `String`, `Box` | `alloc` |
| `Rc`, `Arc` | `alloc` |
| `BTreeMap`, `VecDeque` | `alloc` |
| `format!`, `vec!` | `alloc` |
| `HashMap` | `std` |
| `Mutex`, `thread` | `std` |
| `File`, `TcpStream` | `std` |
| `println!`, `env::args` | `std` |

## Opening lines

| Need | Written as |
|---|---|
| Turn `std` off | `#![no_std]` |
| Open `alloc` | `extern crate alloc;` |
| `Vec` | `use alloc::vec::Vec;` |
| `String`, `to_string` | `use alloc::string::{String, ToString};` |
| `format!` | `use alloc::format;` |
| `vec!` | `use alloc::vec;` |
| `Box` | `use alloc::boxed::Box;` |

## core instead of std

| Habit | In `no_std` |
|---|---|
| `std::mem::swap` | `core::mem::swap` |
| `std::fmt::Display` | `core::fmt::Display` |
| `std::error::Error` | `core::error::Error` |
| `std::time::Duration` | `core::time::Duration` |
| `std::sync::atomic` | `core::sync::atomic` |
| `println!` | Your own output, `core::fmt::Write` |
| Floating `sqrt`, `powf` | Not in `core`; the `libm` crate or integers |

## A library fitting both

Make `std` a feature in the library. `tiny/Cargo.toml`:

```toml
[package]
name = "tiny"
version = "0.1.0"
edition = "2024"

[features]
default = ["std"]
std = []
```

`tiny/src/lib.rs`:

```rust
#![cfg_attr(not(feature = "std"), no_std)]

pub fn double(n: i32) -> i32 {
    n * 2
}

#[cfg(feature = "std")]
pub fn show_double(n: i32) {
    println!("{}", double(n));
}
```

```text
42
```

`cargo build --no-default-features` compiles the same library as `no_std`; we measured it, and it passes. Common crates do the same.
