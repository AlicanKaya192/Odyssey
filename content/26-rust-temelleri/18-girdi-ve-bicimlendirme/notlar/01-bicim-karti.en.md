## The layout of a format string

The inside of the curly braces is written in this order; every part is optional:

```text
{name : fill align sign # 0 width .digits type}
```

## All together

| Written as | Value | Result |
|---|---|---|
| `{}` | `42` | `42` |
| `{name}` | `name = "Ada"` | `Ada` |
| `{0} {1} {0}` | `"a", "b"` | `a b a` |
| `{:.2}` | `3.14159` | `3.14` |
| `{:5}` | `42` | `   42` |
| `{:<5}` | `42` | `42   ` |
| `{:^5}` | `"ab"` | ` ab  ` |
| `{:05}` | `42` | `00042` |
| `{:*^7}` | `"ab"` | `**ab***` |
| `{:+}` | `42` | `+42` |
| `{:>8.2}` | `3.5` | `    3.50` |
| `{:b}` | `10` | `1010` |
| `{:o}` | `10` | `12` |
| `{:x}` `{:X}` | `255` | `ff` `FF` |
| `{:#x}` | `255` | `0xff` |
| `{:08b}` | `10` | `00001010` |
| `{:e}` | `1500.0` | `1.5e3` |
| `{:?}` | `"Ada"` | `"Ada"` |
| `{:#?}` | A tuple, a struct | Several lines |

## The width can come from a variable

If the width or the digits are only known while running, a `$` goes after the name:

```rust
fn main() {
    let width = 6;
    let digits = 2;
    println!("[{:>width$}]", "ab");
    println!("[{:.digits$}]", 3.14159);
    println!("[{:>width$.digits$}]", 3.14159);
}
```

```text
[    ab]
[3.14]
[  3.14]
```

## The macros that write

| Macro | Where it writes | Line ending |
|---|---|---|
| `println!` | Standard output | Yes |
| `print!` | Standard output | No |
| `eprintln!` | Standard error | Yes |
| `eprint!` | Standard error | No |
| `format!` | Does not write, gives a `String` | No |

Error messages are written with `eprintln!`: they stay on screen even if the output is redirected to a file.
