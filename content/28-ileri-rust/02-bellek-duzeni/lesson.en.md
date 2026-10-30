# Memory Layout: repr

How does a struct sit in memory? Most of the time you need not know. But you do when writing your own `Vec`, talking to C or shrinking memory.

## Size and alignment

Every type has a **size** and an **alignment**. Alignment says at which addresses a type can live: if `align_of::<u32>()` is 4, the address must be a multiple of 4. Size is always a multiple of alignment, because items in an array sit side by side.

```rust
struct Empty;

fn main() {
    println!("u8 {} {}", size_of::<u8>(), align_of::<u8>());
    println!("u32 {} {}", size_of::<u32>(), align_of::<u32>());
    println!("u64 {} {}", size_of::<u64>(), align_of::<u64>());
    println!("() {}", size_of::<()>());
    println!("Empty {}", size_of::<Empty>());
    println!("[u32; 3] {}", size_of::<[u32; 3]>());
}
```

```text
u8 1 1
u32 4 4
u64 8 8
() 0
Empty 0
[u32; 3] 12
```

Zero-sized types (`()` and a struct with no fields) truly take no space. `Vec<()>` allocates no memory.

## Field order

Gaps for alignment go between fields. The same three-field struct has different sizes by order. The default Rust layout can **reorder** fields to reduce gaps; `#[repr(C)]` uses your written order and C's rules:

```rust
use std::mem::offset_of;

#[repr(C)]
struct WithC {
    a: u8,
    b: u32,
    c: u8,
}

struct WithRust {
    a: u8,
    b: u32,
    c: u8,
}

#[repr(C)]
struct Sorted {
    b: u32,
    a: u8,
    c: u8,
}

fn main() {
    println!("{}", size_of::<WithC>());
    println!("{}", size_of::<WithRust>());
    println!("{}", size_of::<Sorted>());
    println!("{} {} {}", offset_of!(WithC, a), offset_of!(WithC, b), offset_of!(WithC, c));
}
```

```text
12
8
8
0 4 8
```

Byte by byte:

```text
repr(C)   a . . . b b b b c . . .
Rust      b b b b a c . .
Sorted    b b b b a c . .
```

`.` is a gap. `repr(C)` takes 12 bytes, and the Rust layout 8. In the default layout, field order is **no promise**: it can change with a version, so for writing to a file or passing to C, `repr(C)` is required.

In `repr(C)` you improve the layout yourself: the field with the largest alignment first.

## Packing

`#[repr(packed)]` removes all gaps, but fields become unaligned. Taking a reference to an unaligned field is therefore forbidden:

```rust
#[repr(C, packed)]
struct Tight {
    a: u8,
    b: u32,
}

fn main() {
    let t = Tight { a: 1, b: 2 };
    let r = &t.b;
    println!("{r}");
}
```

```text
error[E0793]: reference to field of packed struct is unaligned
 --> main.rs:9:13
  |
9 |     let r = &t.b;
  |             ^^^^
  |
  = note: this struct is 1-byte aligned, but the type of this field may require higher
    alignment
  = note: creating a misaligned reference is undefined behavior (even if that reference
    is never dereferenced)
  = help: copy the field contents to a local variable, or replace the reference with a
    raw pointer and use `read_unaligned`/`write_unaligned` (loads and stores via `*p`
    must be properly aligned even when using raw pointers)
```

Copying the value first is safe:

```rust
#[repr(C, packed)]
struct Tight {
    a: u8,
    b: u32,
}

fn main() {
    let t = Tight { a: 1, b: 2 };
    let b = t.b;
    println!("{} {b}", size_of::<Tight>());
    println!("{}", t.a);
}
```

```text
5 2
1
```

`#[repr(align(N))]` does the reverse and raises alignment. It is used so branches do not dirty each other's cache lines (the Atomics section).

## Enum layout

An enum carries a **tag** storing which variant it is. But if there are unused values, no tag is needed:

```rust
#[repr(u8)]
#[derive(Clone, Copy)]
enum Level {
    Low = 1,
    High = 9,
}

fn main() {
    println!("{}", size_of::<Option<bool>>());
    println!("{}", size_of::<Option<char>>());
    println!("{}", size_of::<Option<u8>>());
    println!("{}", size_of::<Option<Box<u8>>>());
    println!("{}", size_of::<Level>());
    println!("{} {}", Level::Low as u8, Level::High as u8);
}
```

```text
1
4
2
8
1
1 9
```

| Type | Size | Why |
|---|---|---|
| `Option<bool>` | 1 | `bool` is only 0 and 1, and `None` is 2 |
| `Option<char>` | 4 | `char` has invalid values |
| `Option<u8>` | 2 | `u8` has no free value, so a tag is required |
| `Option<Box<u8>>` | 8 | `Box` cannot be null |

`#[repr(u8)]` ties the tag to a number, read with `as u8`.

## repr(transparent)

It says a one-field wrapper's layout is the same as its field's. So `&[Meters]` can safely convert to `&[f64]`:

```rust
use std::slice;

#[repr(transparent)]
struct Meters(f64);

fn as_numbers(list: &[Meters]) -> &[f64] {
    // SAFETY: Meters has the layout of f64, so the same bytes are valid.
    unsafe { slice::from_raw_parts(list.as_ptr().cast::<f64>(), list.len()) }
}

fn main() {
    let list = [Meters(1.5), Meters(2.5)];
    println!("{:?}", as_numbers(&list));
    println!("{}", size_of::<Meters>());
}
```

```text
[1.5, 2.5]
8
```

## Fat pointers

Some references are two words, because they carry extra information beside the pointer:

```rust
fn main() {
    println!("{}", size_of::<&u8>());
    println!("{}", size_of::<&[u8]>());
    println!("{}", size_of::<&str>());
    println!("{}", size_of::<&dyn std::fmt::Debug>());
    println!("{}", size_of::<Box<[u8]>>());
    println!("{}", size_of::<String>());
    println!("{}", size_of::<Vec<u8>>());
}
```

```text
8
16
16
16
16
24
24
```

| Type | The second word |
|---|---|
| `&[T]`, `&str` | The length |
| `&dyn Trait` | The vtable address |

## Summary

- Size is a multiple of alignment; gaps go between fields.
- The Rust layout reorders fields, and this is no promise.
- `repr(C)`: the written order, C's rules. For files and FFI.
- `repr(packed)`: no gaps, no reference to a field.
- An enum sits without a tag if there is a free value: `Option<&T>`.
- `repr(transparent)`: a wrapper with the same layout as its field.
