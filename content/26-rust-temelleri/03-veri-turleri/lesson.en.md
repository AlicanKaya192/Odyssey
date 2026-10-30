# Data Types

In memory everything is made of bits, 0s and 1s. The same bits can be a number or a letter. A **type**
says what a value represents and what you can do with it.

Rust is a **statically typed** language: the type of every variable is known at compile time. You need
not write it, since the compiler usually works it out itself. But if it cannot, it asks.

```rust
fn main() {
    let x = 2;
    let total: i32 = 40;
    println!("{}", x + total);
}
```

```text
42
```

The `: i32` in `let total: i32 = 40;` is a **type annotation**. We did not write one for `x`; the compiler inferred it.

## Whole numbers

Integer types answer two questions: can it be negative, and how many bits does it hold?

| Bits | Signed (may be negative) | Unsigned (0 and up) |
|---|---|---|
| 8 | `i8` | `u8` |
| 16 | `i16` | `u16` |
| 32 | `i32` | `u32` |
| 64 | `i64` | `u64` |
| 128 | `i128` | `u128` |
| Machine dependent | `isize` | `usize` |

`i` means "integer" and `u` means "unsigned". More bits fit a larger number. You can ask each type for its
limit directly:

```rust
fn main() {
    println!("u8:  {} to {}", u8::MIN, u8::MAX);
    println!("i8:  {} to {}", i8::MIN, i8::MAX);
    println!("i32: {} to {}", i32::MIN, i32::MAX);
}
```

```text
u8:  0 to 255
i8:  -128 to 127
i32: -2147483648 to 2147483647
```

If you write no type, integers are `i32`, which is the right choice for most work. For positions and lengths
Rust uses `usize`: a number large enough to address this machine's memory, 64 bits on a 64-bit computer.

## Overflow: what if the limit is passed?

`u8` holds at most 255. What if we add 1 to 255? If the compiler sees a constant operation it refuses outright. If
the value appears while running, in a development build the program **panics**, meaning it stops with an error message:

```rust
fn main() {
    let text = "hello";
    let mut small = 251u8;
    small += text.len() as u8;
    println!("{small}");
}
```

```text
thread 'main' panicked at main.rs:4:5:
attempt to add with overflow
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

Here `.len()` gives the text's length and `as u8` converts it to `u8`, so the compiler cannot see the number in
advance. In a `--release` build this check is off and the number wraps around (255 + 1 = 0). Because of this
difference it is best to be explicit where overflow is possible:

```rust
fn main() {
    let big: u8 = 250;
    println!("{:?}", big.checked_add(10));
    println!("{}", big.wrapping_add(10));
    println!("{}", big.saturating_add(10));
}
```

```text
None
4
255
```

| Method | What it does |
|---|---|
| `checked_add` | Gives `None` on overflow (`Option`, which we will see later) |
| `wrapping_add` | Wraps around |
| `saturating_add` | Stays at the limit |

## Decimal numbers

There are two types: `f32` and `f64`. The default is `f64`, and that is what you use for most work.

```rust
fn main() {
    let half = 7.0 / 2.0;
    println!("{half}");
    println!("{}", 0.1 + 0.2);
    let difference: f64 = (0.1 + 0.2 - 0.3_f64).abs();
    println!("{}", difference < 0.000001);
}
```

```text
3.5
0.30000000000000004
true
```

Note the second line: `0.1 + 0.2` is not exactly `0.3`. This is not peculiar to Rust; it comes from computers
holding decimals in base two and exists in all languages. So instead of comparing decimals with `==`, you check
whether the difference is very small. For exact calculations such as money, use whole numbers (cents).

## Number types do not mix by themselves

Unlike many languages, Rust does not add an `i32` and an `f64` by itself:

```rust
fn main() {
    let count = 3;
    let price = 2.5;
    println!("{}", count * price);
}
```

```text
error[E0277]: cannot multiply `{integer}` by `{float}`
 --> main.rs:4:26
  |
4 |     println!("{}", count * price);
  |                          ^ no implementation for `{integer} * {float}`
  |
  = help: the trait `Mul<{float}>` is not implemented for `{integer}`
  = help: the following other types implement trait `Mul<Rhs>`:
            `&f128` implements `Mul<f128>`
            `&f128` implements `Mul`
            `&f16` implements `Mul<f16>`
            `&f16` implements `Mul`
            `&f32` implements `Mul<f32>`
            `&f32` implements `Mul`
            `&f64` implements `Mul<f64>`
            `&f64` implements `Mul`
          and 57 others
```

You write the conversion explicitly. `as` is the simplest way:

```rust
fn main() {
    let count = 3;
    let price = 2.5;
    println!("{}", count as f64 * price);
    println!("{}", 9.99_f64 as i32);
    println!("{}", 300_i32 as u8);
}
```

```text
7.5
9
44
```

Note the last line. When converting to a shorter type, `as` **silently cuts the value**: 300 does not fit in `u8` and
becomes 44. Converting a decimal to an integer discards the fractional part rather than rounding. So use `as` when you
are sure the result fits. We will see safe conversions later.

## Logical values: bool

`bool` takes only two values: `true` and `false`. It is the result of comparisons.

```rust
fn main() {
    let age = 20;
    let adult = age >= 18;
    println!("{adult}");
    println!("{}", adult && age < 30);
    println!("{}", !adult || age == 20);
}
```

```text
true
true
true
```

`&&` means "and", `||` means "or", `!` means "not".

## Characters: char

`char` is a single character and is written with **single quotes**. In Rust a `char` is 4 bytes and can hold letters
of any alphabet and emoji too:

```rust
fn main() {
    let letter = 'R';
    let crab = '\u{1F980}';
    println!("{letter} {crab}");
    println!("{}", std::mem::size_of::<char>());
}
```

```text
R 🦀
4
```

Single quotes make a `char`, double quotes make text: `'a'` and `"a"` are different types.

## Several values: tuples

A **tuple** gathers a fixed number of values of different types into one value:

```rust
fn main() {
    let point = (3, 4.5, true);
    println!("{}", point.0);
    println!("{:?}", point);
    let (x, y, on) = point;
    println!("{x} {y} {on}");
}
```

```text
3
(3, 4.5, true)
3 4.5 true
```

You reach the parts with `.0`, `.1` or by opening it with `let`. Opening it is called **destructuring**. The `{:?}`
format prints the tuple as it is; plain `{}` does not accept a tuple.

The tuple with no values, `()`, is a special type called **unit**: it means "no meaningful value".

## Fixed lists: arrays

An **array** is a **fixed number** of values of the same type:

```rust
fn main() {
    let days: [i32; 3] = [10, 20, 30];
    println!("{}", days[0]);
    println!("{}", days.len());
    println!("{:?}", days);
    let zeros = [0; 4];
    println!("{:?}", zeros);
}
```

```text
10
3
[10, 20, 30]
[0, 0, 0, 0]
```

Its type is `[i32; 3]`: "3 `i32`s". Positions start at 0. The size is part of the type, so an array cannot grow or
shrink. The list that can grow is `Vec`, which we will see later.

A position outside the array stops the program. In this way Rust prevents reading neighbouring memory:

```rust
fn main() {
    let days = [10, 20, 30];
    let position = days.len() + 1;
    println!("{}", days[position]);
}
```

```text
thread 'main' panicked at main.rs:4:20:
index out of bounds: the len is 3 but the index is 4
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

This **panic** is an error, but a controlled one: rather than continuing with nonsense data, the program stops and says where.

## Summary

- Every value's type is known at compile time; the compiler usually infers it.
- Integers are `i32`, `u8`, `usize` and so on; the default is `i32`. Overflow panics in a development build.
- Decimals are `f64`; `0.1 + 0.2` is not exactly `0.3`.
- Numbers do not mix by themselves; `as` is an explicit conversion and may cut silently.
- `bool`, single-quoted `char`, and fixed-size tuples and arrays are the basic compound types.
