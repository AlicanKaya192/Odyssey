## Order of precedence

The higher one runs first. Those on the same row run left to right; assignment runs right to left.

| Order | Operators |
|---|---|
| 1 | Method call `x.pow(2)`, array access `a[0]` |
| 2 | Unary `-x`, `!x` |
| 3 | `as` |
| 4 | `*` `/` `%` |
| 5 | `+` `-` |
| 6 | `<<` `>>` |
| 7 | `&` |
| 8 | `^` |
| 9 | <code>&#124;</code> |
| 10 | `==` `!=` `<` `>` `<=` `>=` |
| 11 | `&&` |
| 12 | <code>&#124;&#124;</code> |
| 13 | `=` `+=` `-=` `*=` `/=` `%=` |

Do not memorise this. If in doubt, write parentheses.

## Bit operators

These operators look at the number written in binary and work bit by bit. You rarely need them at the start; they are
here so that you see why `^` is not a power.

```rust
fn main() {
    println!("{}", 12 & 10);
    println!("{}", 12 | 10);
    println!("{}", 12 ^ 10);
    println!("{}", 1 << 3);
    println!("{}", 16 >> 2);
    println!("{}", !0_u8);
}
```

```text
8
14
6
8
4
255
```

| Operator | What it does | Example |
|---|---|---|
| `&` | 1 if both bits are 1 | `12 & 10` = 8 |
| <code>&#124;</code> | 1 if either is 1 | <code>12 &#124; 10</code> = 14 |
| `^` | 1 if exactly one is 1 | `12 ^ 10` = 6 |
| `<<` | Shifts left (like multiplying by 2) | `1 << 3` = 8 |
| `>>` | Shifts right (like dividing by 2) | `16 >> 2` = 4 |
| `!` | Flips the bits | `!0_u8` = 255 |

## `&` and `&&` are not the same

`&` also works on `bool` values but does **not** short circuit: it evaluates both sides. So the safe form from the lesson
panics with a single `&`:

```rust
fn main() {
    let items = "".len();
    println!("{}", (items != 0) & (10 / items > 1));
}
```

```text
thread 'main' panicked at main.rs:3:36:
attempt to divide by zero
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

When joining conditions, always write `&&` and `||`.
