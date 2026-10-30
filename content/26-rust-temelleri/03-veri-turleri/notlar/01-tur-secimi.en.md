## Which type to choose?

| Need | Type | Why |
|---|---|---|
| An ordinary whole number | `i32` | The default, enough for most work |
| A position, a length | `usize` | `.len()` and array access want it |
| A byte, a small positive value | `u8` | 0–255 |
| A very large number, a timestamp | `i64` / `u64` | Around 9 quintillion |
| A decimal | `f64` | Precise and fast |
| Yes/no | `bool` | |
| One letter | `char` | Four bytes, holds any alphabet |

## Sizes in bytes

```rust
fn main() {
    use std::mem::size_of;
    println!("u8:    {}", size_of::<u8>());
    println!("i32:   {}", size_of::<i32>());
    println!("f64:   {}", size_of::<f64>());
    println!("char:  {}", size_of::<char>());
    println!("bool:  {}", size_of::<bool>());
    println!("usize: {}", size_of::<usize>());
}
```

```text
u8:    1
i32:   4
f64:   8
char:  4
bool:  1
usize: 8
```

`std::mem::size_of` says how many bytes a type takes in memory. This was measured on this machine; `usize` is 8 bytes on
a 64-bit computer.

## Ways to write numbers

| Written | Value | Meaning |
|---|---|---|
| `1_000_000` | one million | Underscores aid reading |
| `0xFF` | 255 | Hexadecimal |
| `0b1010` | 10 | Binary |
| `0o17` | 15 | Octal |
| `b'A'` | 65 | The byte value of a character |
| `7u8` | 7 | The type written on the number |
| `2.5e3` | 2500.0 | Scientific notation |

## Where are the text types?

Text (`String`, `&str`) is not here, because it cannot be explained without understanding ownership. Section eight deals with it on its own.
