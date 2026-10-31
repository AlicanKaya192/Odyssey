## Used every day

| What you want | Written as | For `n = 4728` |
|---|---|---|
| Is it even? | `n % 2 == 0` | `true` |
| Is it odd? | `n % 2 != 0` | `false` |
| Does it divide by 5? | `n % 5 == 0` | `false` |
| Last digit | `n % 10` | 8 |
| Second to last digit | `n / 10 % 10` | 2 |
| Third to last digit | `n / 100 % 10` | 7 |

Do not test for odd with `n % 2 == 1`: `-3 % 2` is `-1` and the condition comes out wrong. `!= 0` is right for every number.

## Splitting digits and wrapping around

```rust
fn main() {
    let n = 4728;
    println!("{}", n % 10);
    println!("{}", n / 10 % 10);
    println!("{}", n / 100 % 10);
    println!("{}", (0 - 1) % 7);
    println!("{}", (0_i32 - 1).rem_euclid(7));
}
```

```text
8
2
7
-1
6
```

The last two lines ask the same question: "Which day is one day before Monday (0)?" `%` gives a negative number,
`rem_euclid` gives the right day, 6 (Sunday). When a wrapping count can go below zero, use `rem_euclid`.

## Remainder by zero

Like dividing by zero, taking a remainder by zero stops the program:

```rust
fn main() {
    let items = "".len();
    println!("{}", 10 % items);
}
```

```text
thread 'main' panicked at main.rs:3:20:
attempt to calculate the remainder with a divisor of zero
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```
