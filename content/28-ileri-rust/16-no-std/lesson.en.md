# no_std

Every program we have written so far ran on top of an operating system: it opened files, started branches, wrote to the screen. On the processor of a washing machine, or in the operating system itself, none of that exists. Rust works there too, because its standard library is layered.

## Three layers

| Layer | What it requires | What it contains |
|---|---|---|
| `core` | Nothing | `Option`, `Result`, slices, `Iterator`, `fmt`, atomics |
| `alloc` | A memory allocator | `Vec`, `String`, `Box`, `Arc`, `BTreeMap` |
| `std` | An operating system | Files, branches, networks, environment variables, `HashMap`, `println!` |

The upper uses the lower. `std::option::Option` is really `core::option::Option` re-exported, so you have been using `core` without noticing.

## The first no_std library

`#![no_std]` links a crate to `core` instead of `std`. To try it easily in this section, we write a `no_std` library and call it from an ordinary program. The root `Cargo.toml`:

```toml
[package]
name = "app"
version = "0.1.0"
edition = "2024"

[dependencies]
tiny = { path = "tiny" }
```

`tiny/src/lib.rs`:

```rust
#![no_std]

pub fn clamp_percent(value: i32) -> u8 {
    if value < 0 {
        0
    } else if value > 100 {
        100
    } else {
        value as u8
    }
}

pub fn first_word(text: &str) -> &str {
    text.split(' ').next().unwrap_or("")
}
```

`src/main.rs`:

```rust
use tiny::{clamp_percent, first_word};

fn main() {
    println!("{}", clamp_percent(150));
    println!("{}", first_word("hello there"));
}
```

```text
100
hello
```

Built-in types, slices, `Option` and `split` are all in `core`, so we missed nothing. The ordinary program uses this library without trouble, because `std` sits above it.

## What is lost?

The compiler checks the boundary itself. Touching `std`:

```rust
#![no_std]

use std::collections::HashMap;

pub fn empty() -> HashMap<u8, u8> {
    HashMap::new()
}
```

```text
error[E0433]: cannot find module or crate `std` in this scope
 --> tiny/src/lib.rs:3:5
  |
3 | use std::collections::HashMap;
  |     ^^^ use of unresolved module or unlinked crate `std`
  |
  = help: if you wanted to use a crate named `std`, use `cargo add std` to add it to
    your `Cargo.toml`

For more information about this error, try `rustc --explain E0433`.
```

The compiler's `cargo add std` suggestion is misleading here: `std` is not a crate to add. The solution is to delete the line or to remove `#![no_std]`.

`Vec` no longer comes ready:

```rust
#![no_std]

pub fn numbers() -> Vec<u32> {
    Vec::new()
}
```

```text
error[E0425]: cannot find type `Vec` in this scope
 --> tiny/src/lib.rs:3:21
  |
3 | pub fn numbers() -> Vec<u32> {
  |                     ^^^ not found in this scope

error[E0433]: cannot find type `Vec` in this scope
 --> tiny/src/lib.rs:4:5
  |
4 |     Vec::new()
  |     ^^^ use of undeclared type `Vec`

Some errors have detailed explanations: E0425, E0433.
For more information about an error, try `rustc --explain E0425`.
```

Writing to the screen is gone too, because "the screen" is the operating system's concept:

```rust
#![no_std]

pub fn say() {
    println!("hello");
}
```

```text
error: cannot find macro `println` in this scope
 --> tiny/src/lib.rs:4:5
  |
4 |     println!("hello");
  |     ^^^^^^^
```

## alloc: if there is an allocator

With an allocator, `Vec` and `String` come back. The `alloc` crate comes with the compiler but is opened by hand:

```rust
#![no_std]

extern crate alloc;

use alloc::string::{String, ToString};
use alloc::vec::Vec;

pub fn words(text: &str) -> Vec<String> {
    text.split(' ').map(|word| word.to_string()).collect()
}
```

```text
["one", "two"]
```

`HashMap` is missing here too, because its default hasher goes to the operating system for randomness. The ordered map `alloc::collections::BTreeMap` can be used.

## Living without allocation

Small devices may have no allocator at all, and even with one, "out of memory" may be unacceptable. The solution: fix the capacity at compile time. Instead of allocating, use a const generic:

```rust
#![no_std]

pub struct Stack<const N: usize> {
    items: [i32; N],
    len: usize,
}

impl<const N: usize> Stack<N> {
    pub const fn new() -> Self {
        Stack { items: [0; N], len: 0 }
    }

    pub fn push(&mut self, value: i32) -> Result<(), i32> {
        if self.len == N {
            return Err(value);
        }
        self.items[self.len] = value;
        self.len += 1;
        Ok(())
    }

    pub fn as_slice(&self) -> &[i32] {
        &self.items[..self.len]
    }
}
```

```rust
use tiny::Stack;

static EMPTY: Stack<2> = Stack::new();

fn main() {
    let mut stack = Stack::<2>::new();
    println!("{:?}", stack.push(1));
    println!("{:?}", stack.push(2));
    println!("{:?}", stack.push(3));
    println!("{:?} {:?}", stack.as_slice(), EMPTY.as_slice());
    println!("{}", size_of::<Stack<2>>());
}
```

```text
Ok(())
Ok(())
Err(3)
[1, 2] []
16
```

- The capacity is part of the type, and the size is known in advance: 2 `i32`s and one `usize`, 16 bytes.
- When full, no panic and no allocation: `Err(value)` gives the value back.
- Thanks to `const fn`, it can be built inside a `static`, ready before the program starts.

Producing text does not need `String` either. `write!` can write to anything implementing `core::fmt::Write`:

```rust
#![no_std]

use core::fmt::{self, Write};

pub struct Buffer<'a> {
    bytes: &'a mut [u8],
    len: usize,
}

impl<'a> Buffer<'a> {
    pub fn new(bytes: &'a mut [u8]) -> Self {
        Buffer { bytes, len: 0 }
    }

    pub fn as_bytes(&self) -> &[u8] {
        &self.bytes[..self.len]
    }
}

impl Write for Buffer<'_> {
    fn write_str(&mut self, text: &str) -> fmt::Result {
        let end = self.len + text.len();
        if end > self.bytes.len() {
            return Err(fmt::Error);
        }
        self.bytes[self.len..end].copy_from_slice(text.as_bytes());
        self.len = end;
        Ok(())
    }
}

pub fn format_reading(out: &mut Buffer, celsius: i32) -> fmt::Result {
    write!(out, "temp={celsius}C")
}
```

```rust
use tiny::{Buffer, format_reading};

fn main() {
    let mut storage = [0u8; 16];
    let mut buffer = Buffer::new(&mut storage);
    println!("{:?}", format_reading(&mut buffer, 21));
    println!("{}", str::from_utf8(buffer.as_bytes()).unwrap());

    let mut small = [0u8; 3];
    let mut buffer = Buffer::new(&mut small);
    println!("{:?}", format_reading(&mut buffer, 21));
}
```

```text
Ok(())
temp=21C
Err(Error)
```

Text that did not fit returned an error, and the program is still standing. This pattern appears all the time in embedded code.

## Seeing the memory allocator

In a `no_std` program you choose the allocator; `#[global_allocator]` is the way, and it also works in a `std` program. Let us count all allocations:

```rust
use std::alloc::{GlobalAlloc, Layout, System};
use std::sync::atomic::{AtomicUsize, Ordering};

struct Counting;

static COUNT: AtomicUsize = AtomicUsize::new(0);

// SAFETY: every call is passed on to the system allocator unchanged.
unsafe impl GlobalAlloc for Counting {
    unsafe fn alloc(&self, layout: Layout) -> *mut u8 {
        COUNT.fetch_add(1, Ordering::Relaxed);
        unsafe { System.alloc(layout) }
    }

    unsafe fn dealloc(&self, pointer: *mut u8, layout: Layout) {
        unsafe { System.dealloc(pointer, layout) }
    }
}

#[global_allocator]
static ALLOCATOR: Counting = Counting;

fn count_of(work: impl FnOnce()) -> usize {
    let before = COUNT.load(Ordering::Relaxed);
    work();
    COUNT.load(Ordering::Relaxed) - before
}

fn main() {
    println!("array: {}", count_of(|| {
        let values = [1u8; 64];
        std::hint::black_box(values);
    }));
    println!("one box: {}", count_of(|| {
        std::hint::black_box(Box::new(1u8));
    }));
    println!("grown: {}", count_of(|| {
        let mut values = Vec::with_capacity(4);
        values.extend_from_slice(&[1u8, 2, 3, 4]);
        std::hint::black_box(values);
    }));
}
```

```text
array: 0
one box: 1
grown: 1
```

The array made no allocation, since it sits on the stack. On a small device you write the same `GlobalAlloc` to give memory from a fixed region. It is an `unsafe impl`, because an allocator that does not keep its size and alignment promises breaks the whole program.

## Summary

- `core`: requires nothing. `alloc`: requires an allocator. `std`: requires an operating system.
- `#![no_std]` has the compiler check the boundary.
- `extern crate alloc;` brings `Vec` and `String` back.
- Without allocation: fixed capacity with a const generic, a fixed buffer with `core::fmt::Write`.
- `#[global_allocator]` chooses the type managing all allocations.
