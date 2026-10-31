# Operators

When you write `2 + 3`, the `+` is an **operator**: a sign that says "do this with these values". This section gathers
every operator that calculates, compares and combines conditions. Most are the same in every language, but Rust has a
few surprises: there is no power operator and no `++`.

## Arithmetic

```rust
fn main() {
    println!("{}", 7 + 2);
    println!("{}", 7 - 2);
    println!("{}", 7 * 2);
    println!("{}", 7 / 2);
    println!("{}", 7 % 2);
}
```

```text
9
5
14
3
1
```

| Operator | Meaning | Example | Result |
|---|---|---|---|
| `+` | Addition | `7 + 2` | 9 |
| `-` | Subtraction | `7 - 2` | 5 |
| `*` | Multiplication | `7 * 2` | 14 |
| `/` | Division | `7 / 2` | 3 |
| `%` | Remainder | `7 % 2` | 1 |

Look at the fourth row: `7 / 2` is 3, not 3.5.

## Integer division

If both sides are integers the result is an integer too, and the fractional part is discarded. For a decimal result you
convert both sides **before** dividing:

```rust
fn main() {
    let a = 7;
    let b = 2;
    println!("{}", a / b);
    println!("{}", a as f64 / b as f64);
    println!("{}", (a / b) as f64);
}
```

```text
3
3.5
3
```

The third line gave 3 again: `(a / b)` divides first, the decimals are lost at that moment, and converting afterwards no
longer helps.

## Remainder: `%`

`%` gives what is left over from a division. At first it looks rarely useful, but you meet it all the time:

```rust
fn main() {
    let n = 472;
    println!("{}", n % 2 == 0);
    println!("{}", n % 10);
    let minutes = 135;
    println!("{} h {} min", minutes / 60, minutes % 60);
    println!("{}", (5 + 4) % 7);
}
```

```text
true
2
2 h 15 min
2
```

| Question | Written as | Why |
|---|---|---|
| Is the number even? | `n % 2 == 0` | Nothing left when divided by two |
| What is the last digit? | `n % 10` | What is left when divided by ten |
| How many hours and minutes? | `m / 60` and `m % 60` | The quotient is hours, the remainder minutes |
| Nine days after Monday? | `(0 + 9) % 7` | Counting that wraps around |

With negative numbers the remainder takes the sign of the dividend. If you always want zero or a positive remainder,
there is `rem_euclid`. `%` also works on decimals:

```rust
fn main() {
    println!("{}", -7 / 2);
    println!("{}", -7 % 2);
    println!("{}", (-7_i32).rem_euclid(2));
    println!("{}", 7.5 % 2.0);
}
```

```text
-3
-1
1
1.5
```

## Powers: no operator

In many languages a power is written with `**` or `^`. Rust has no power operator; you call a method: `pow` on integers,
and on decimals `powi` for an integer power and `powf` for a decimal one.

```rust
fn main() {
    println!("{}", 2_i32.pow(10));
    println!("{}", 2.0_f64.powi(3));
    println!("{}", 9.0_f64.powf(0.5));
    println!("{}", 2 ^ 3);
}
```

```text
1024
8
3
1
```

The last line is a trap: `2 ^ 3` compiles and gives **1**. `^` is not a power; it is another operator that compares bits.
The compiler does not warn, because the code is valid.

## Compound assignment

Changing a variable based on its own value is so common that it has a short form. `score += 5` means
`score = score + 5`. The variable must be `mut`.

```rust
fn main() {
    let mut score = 10;
    score += 5;
    println!("{score}");
    score -= 3;
    println!("{score}");
    score *= 2;
    println!("{score}");
    score /= 4;
    println!("{score}");
    score %= 4;
    println!("{score}");
}
```

```text
15
12
24
6
2
```

Rust has no `++` or `--`. If you write it out of habit from another language, the compiler tells you what to do:

```rust
fn main() {
    let mut x = 1;
    x++;
    println!("{x}");
}
```

```text
error: Rust has no postfix increment operator
 --> main.rs:3:6
  |
3 |     x++;
  |      ^^ not a valid postfix operator
  |
help: use `+= 1` instead
  |
3 -     x++;
3 +     x += 1;
  |
```

## Comparison

Comparison operators look at two values and produce a `bool`. Careful: `=` assigns, `==` compares.

```rust
fn main() {
    println!("{}", 5 == 5);
    println!("{}", 5 != 5);
    println!("{}", 3 < 7);
    println!("{}", 7 <= 7);
    println!("{}", "apple" == "apple");
    println!("{}", "apple" < "banana");
    println!("{}", 'a' < 'b');
}
```

```text
true
false
true
true
true
true
true
```

| Operator | Meaning |
|---|---|
| `==` | Equal |
| `!=` | Not equal |
| `<` `>` | Less than, greater than |
| `<=` `>=` | Less or equal, greater or equal |

Text is compared in dictionary order. Both sides must be of the **same type**; here too Rust does not convert by itself:

```rust
fn main() {
    let a: i32 = 5;
    let b: i64 = 5;
    println!("{}", a == b);
}
```

```text
error[E0308]: mismatched types
 --> main.rs:4:25
  |
4 |     println!("{}", a == b);
  |                    -    ^ expected `i32`, found `i64`
  |                    |
  |                    expected because this is `i32`
  |
help: you can convert `a` from `i32` to `i64`, matching the type of `b`
  |
4 |     println!("{}", i64::from(a) == b);
  |                    ++++++++++ +
```

The fix is `a as i64 == b`. Comparisons do not chain as they do in mathematics:

```rust
fn main() {
    let x = 5;
    println!("{}", 1 < x < 10);
}
```

```text
error: comparison operators cannot be chained
 --> main.rs:3:22
  |
3 |     println!("{}", 1 < x < 10);
  |                      ^   ^
  |
help: split the comparison into two
  |
3 |     println!("{}", 1 < x && x < 10);
  |                          ++++
```

The right way is to split the condition in two and join it with `&&`:

```rust
fn main() {
    let x = 5;
    println!("{}", 1 < x && x < 10);
}
```

```text
true
```

## Logic: `&&`, `||`, `!`

| Operator | Meaning | When it is `true` |
|---|---|---|
| `&&` | And | Both sides are `true` |
| <code>&#124;&#124;</code> | Or | At least one is `true` |
| `!` | Not | The value is `false` |

```rust
fn main() {
    let age = 20;
    let member = false;
    println!("{}", age >= 18 && member);
    println!("{}", age >= 18 || member);
    println!("{}", !member);
}
```

```text
false
true
true
```

`&&` and `||` **short circuit**: if the left side settles the result, the right side never runs. This is not a speed
detail but a safety tool. Dividing an integer by zero stops the program:

```rust
fn main() {
    let items = "".len();
    println!("{}", 10 / items);
}
```

```text
thread 'main' panicked at main.rs:3:20:
attempt to divide by zero
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

If you check for zero first, the division never runs:

```rust
fn main() {
    let items = "".len();
    println!("{}", items != 0 && 10 / items > 1);
    println!("{}", items == 0 || 10 / items > 1);
}
```

```text
false
true
```

The `"".len()` here is the length of an empty text, which is 0. We wrote zero in this roundabout way because the compiler
rejects `10 / 0` directly.

## Which comes first?

As in mathematics, multiplication comes before addition. If the order gets confusing in an expression, write parentheses;
it runs correctly and the reader does not have to think.

```rust
fn main() {
    println!("{}", 2 + 3 * 4);
    println!("{}", (2 + 3) * 4);
    println!("{}", 10 - 4 - 3);
    println!("{}", true || false && false);
    println!("{}", (true || false) && false);
    println!("{}", -2_i32.pow(2));
    println!("{}", (-2_i32).pow(2));
}
```

```text
14
20
3
true
false
-4
4
```

Look at two results. Because `&&` comes before `||`, the fourth line gave `true`. In the last two lines the method call
comes before the minus sign: `-2_i32.pow(2)` means "the negative of the square of 2". The full table is in the notes.

## Summary

- `+ - * / %`: `/` drops the decimals on integers, `%` gives the remainder.
- For decimal division both sides are converted **before dividing**: `a as f64 / b as f64`.
- There is no power operator: `pow`, `powi`, `powf`. `^` is not a power.
- `+=`, `-=`, `*=`, `/=`, `%=` exist; `++` does not.
- `==`, `!=`, `<`, `>`, `<=`, `>=` produce a `bool`; both sides must be the same type, and they do not chain.
- `&&` and `||` short circuit, which protects you from errors such as dividing by zero.
