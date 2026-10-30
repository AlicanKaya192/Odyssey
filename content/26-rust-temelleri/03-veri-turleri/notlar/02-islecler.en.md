## Arithmetic

```rust
fn main() {
    println!("{}", 7 + 2);
    println!("{}", 7 - 2);
    println!("{}", 7 * 2);
    println!("{}", 7 / 2);
    println!("{}", 7 % 2);
    println!("{}", 7.0 / 2.0);
    println!("{}", -7 / 2);
    println!("{}", -7 % 2);
}
```

```text
9
5
14
3
1
3.5
-3
-1
```

**Integer division discards the fractional part:** `7 / 2` is `3`, not `3.5`. For a decimal result write `7.0 / 2.0`. `%` gives the remainder.

Careful with negative numbers: `-7 / 2` is `-3` and `-7 % 2` is `-1`. The result is truncated towards zero.

## Common number methods

| Method | Example | Result |
|---|---|---|
| `abs` | `(-5_i32).abs()` | 5 |
| `pow` | `2_i32.pow(10)` | 1024 |
| `min` / `max` | `3.min(9)` | 3 |
| `sqrt` | `9.0_f64.sqrt()` | 3.0 |
| `round` | `2.5_f64.round()` | 3.0 |
| `floor` / `ceil` | `2.5_f64.floor()` | 2.0 |

When calling a method you may need to state the number's type: `9.0.sqrt()` does not compile because the compiler cannot tell whether it is `f32` or `f64`. So you write `9.0_f64`.

## Comparison and logic

| Sign | Meaning |
|---|---|
| `==` `!=` | Equal, not equal |
| `<` `>` `<=` `>=` | Less, greater, less or equal, greater or equal |
| `&&` <code>&#124;&#124;</code> `!` | And, or, not |

`&&` and `||` short-circuit: if the left side decides the result, the right side never runs.

## In a comparison the types must match

`let a: i32 = 5; let b: i64 = 5; a == b` does not compile. Here too Rust does not turn `i32` into `i64` by itself: write `a as i64 == b`.
