# Performance

Rust is fast, but a fast program does not come by itself. This section has three things: measuring correctly, removing needless work, and arranging memory to suit the processor.

The times in this section were measured **on this computer**, and yours will differ. What matters is not the numbers but the ratios between them. The exercises do not look at time either: they count allocations and measure sizes, and those numbers are the same on every machine.

## First, measure correctly

A debug build does not optimize, because its aim is fast compiling and debugging. The same code in two profiles:

```rust
use std::hint::black_box;
use std::time::Instant;

fn main() {
    let start = Instant::now();
    let mut total = 0u64;
    for i in 0..50_000_000u64 {
        total = total.wrapping_add(black_box(i));
    }
    println!("total {total}");
    println!("time: {} ms", start.elapsed().as_millis());
}
```

```text
$ cargo run
total 1249999975000000
time: 384 ms
```

```text
$ cargo run --release
total 1249999975000000
time: 20 ms
```

Before looking at a program you find slow, make sure you ran it with `--release`. A measurement in debug says nothing.

The second trap goes the other way. The compiler removes work whose result is unused:

```rust
use std::hint::black_box;
use std::time::Instant;

fn main() {
    let start = Instant::now();
    let mut total = 0u64;
    for i in 0..500_000_000u64 {
        total = total.wrapping_add(i);
    }
    println!("unused: {} ms", start.elapsed().as_millis());

    let start = Instant::now();
    let mut total = 0u64;
    for i in 0..500_000_000u64 {
        total = total.wrapping_add(black_box(i));
    }
    println!("{total}");
    println!("measured: {} ms", start.elapsed().as_millis());
}
```

```text
unused: 0 ms
124999999750000000
measured: 185 ms
```

The first loop was not measured, because it does not exist: the compiler removed it. `black_box` says "act as if you do not know this value", and stops the work being removed. In measuring code, pass values through `black_box`.

The third rule: look where the time goes. A program usually spends most of its time in a small region (a **hot spot**). Improvement without measuring mostly fixes places where no time goes.

## Allocations

Allocating memory is relatively expensive, and it can be counted. We use the counting allocator from the last section; it now counts `realloc` too:

```rust
fn main() {
    println!("push: {}", count_of(|| {
        let mut values = Vec::new();
        for i in 0..1000u32 {
            values.push(i);
        }
        black_box(values);
    }));
    println!("with_capacity: {}", count_of(|| {
        let mut values = Vec::with_capacity(1000);
        for i in 0..1000u32 {
            values.push(i);
        }
        black_box(values);
    }));
}
```

```text
push: 9
with_capacity: 1
```

When a `Vec` fills up, it takes a bigger place and moves. If you know the size, `with_capacity` brings it down to one allocation.

A `format!` in a loop produces a new `String` each round. Clearing and reusing one buffer does the same job:

```rust
use std::fmt::Write;

fn main() {
    println!("format!: {}", count_of(|| {
        for i in 0..1000 {
            black_box(format!("line {i}"));
        }
    }));
    println!("one buffer: {}", count_of(|| {
        let mut buffer = String::with_capacity(32);
        for i in 0..1000 {
            buffer.clear();
            write!(buffer, "line {i}").unwrap();
            black_box(&buffer);
        }
    }));
}
```

```text
format!: 1000
one buffer: 1
```

`clear` keeps the capacity and does not free memory. The cheapest allocation is the one never made:

```rust
fn main() {
    let words = vec![String::from("one"), String::from("two"), String::from("three")];
    println!("clone: {}", count_of(|| {
        let mut total = 0;
        for word in &words {
            let copy = word.clone();
            total += copy.len();
        }
        black_box(total);
    }));
    println!("borrow: {}", count_of(|| {
        let mut total = 0;
        for word in &words {
            total += word.len();
        }
        black_box(total);
    }));
}
```

```text
clone: 3
borrow: 0
```

Iterators, slices and `&str` make most copies needless. Where a copy is only sometimes needed, use `Cow`: it borrows if nothing changes, and copies if something does.

## Size

The smaller a struct, the more fit in memory:

```rust
struct Mixed {
    a: u8,
    b: u32,
    c: u8,
}

#[repr(C)]
struct MixedC {
    a: u8,
    b: u32,
    c: u8,
}

enum Heavy {
    Ping,
    Blob([u8; 256]),
}

enum Light {
    Ping,
    Blob(Box<[u8; 256]>),
}

fn main() {
    println!("Mixed {}", size_of::<Mixed>());
    println!("MixedC {}", size_of::<MixedC>());
    println!("Option<u32> {}", size_of::<Option<u32>>());
    println!("Option<Box<u8>> {}", size_of::<Option<Box<u8>>>());
    println!("String {}", size_of::<String>());
    println!("Heavy {}", size_of::<Heavy>());
    println!("Light {}", size_of::<Light>());
    let _ = (Heavy::Ping, Light::Ping, Heavy::Blob([0; 256]));
    let _ = Light::Blob(Box::new([0; 256]));
    let m = Mixed { a: 1, b: 2, c: 3 };
    let n = MixedC { a: 1, b: 2, c: 3 };
    let _ = (m.a, m.b, m.c, n.a, n.b, n.c);
}
```

```text
Mixed 8
MixedC 12
Option<u32> 8
Option<Box<u8>> 8
String 24
Heavy 257
Light 8
```

Each line has a lesson:

- `Mixed` 8, `MixedC` 12: Rust rearranges fields to cut padding; `repr(C)` keeps the written order.
- `Option<u32>` 8: showing `None` needed a separate field.
- `Option<Box<u8>>` 8: a `Box` can never be null, so Rust uses the null pointer for `None`.
- `Heavy` 257: each value takes as much as the biggest variant, even `Ping`.
- `Light` 8: with the big variant in a `Box`, only a pointer remains.

## The cache: memory order is speed

A processor reads memory in small pieces and keeps them in a nearby cache. So reading data sitting side by side is much cheaper than jumping far away. The same sum, the same number of operations:

```rust
use std::hint::black_box;
use std::time::Instant;

const SIZE: usize = 4000;

fn main() {
    let grid = vec![1u32; SIZE * SIZE];

    let start = Instant::now();
    let mut sum = 0u32;
    for row in 0..SIZE {
        for column in 0..SIZE {
            sum = sum.wrapping_add(black_box(grid[row * SIZE + column]));
        }
    }
    black_box(sum);
    println!("rows: {} ms", start.elapsed().as_millis());

    let start = Instant::now();
    let mut sum = 0u32;
    for column in 0..SIZE {
        for row in 0..SIZE {
            sum = sum.wrapping_add(black_box(grid[row * SIZE + column]));
        }
    }
    black_box(sum);
    println!("columns: {} ms", start.elapsed().as_millis());
}
```

```text
rows: 7 ms
columns: 104 ms
```

The table sits in memory row by row. Walking by rows always goes to the neighbour; walking by columns skips 4000 elements each step.

In the code we passed each read through `black_box`. Without it, this comes out:

```text
rows: 3 ms
columns: 3 ms
```

The difference vanished: for a sum this simple, the compiler managed to bring both to the same speed. But once the inside of the loop gets complex, you cannot rely on that help. Two lessons together: memory order matters, and you cannot say "this is surely slow" without measuring.

The same idea holds for structs. Walking one field of a struct with 16 fields also pulls the other 15 into the cache:

```rust
use std::hint::black_box;
use std::time::Instant;

#[derive(Clone)]
struct Particle {
    x: f32,
    other: [f32; 15],
}

const COUNT: usize = 5_000_000;

fn main() {
    let together = vec![Particle { x: 1.0, other: [0.0; 15] }; COUNT];
    let only_x = vec![1.0f32; COUNT];

    let start = Instant::now();
    let sum: f32 = together.iter().map(|p| p.x).sum();
    black_box(sum);
    println!("together: {} ms", start.elapsed().as_millis());

    let start = Instant::now();
    let sum: f32 = only_x.iter().sum();
    black_box(sum);
    println!("separate: {} ms", start.elapsed().as_millis());
    black_box(&together[0].other);
}
```

```text
together: 16 ms
separate: 4 ms
```

This layout is called **SoA** (struct of arrays). It is not always right: if you work with all fields of an item, an array of structs is better. Look at which fields the work touches.

## Are iterators slow?

```rust
use std::hint::black_box;
use std::time::Instant;

fn main() {
    let values = black_box(vec![1u64; 50_000_000]);

    let start = Instant::now();
    let mut sum = 0u64;
    for i in 0..values.len() {
        sum += values[i];
    }
    black_box(sum);
    println!("index: {} ms", start.elapsed().as_millis());

    let start = Instant::now();
    let sum: u64 = values.iter().sum();
    black_box(sum);
    println!("iterator: {} ms", start.elapsed().as_millis());
}
```

```text
index: 24 ms
iterator: 23 ms
```

No. After optimization an iterator is as fast as a hand-written loop, and often removes the bounds check too. Write the readable one; do not convert to the "fast" one without measuring.

## The algorithm first

All of these are constant factors. No cache trick saves an O(n²) algorithm. The order is: measure, look at the algorithm, then allocations, finally layout. Stop when you reach the target; unreadable code is a cost too.

## Summary

- Measure only with `--release`; `black_box` stops work being removed.
- Time is in hot spots; do not improve without measuring.
- `with_capacity`, a reused buffer, borrowing, `Cow`.
- `Box` shrinks a big variant; `Option<Box<T>>` is free.
- Walk in memory order; consider separate arrays for one field.
- The algorithm first.
