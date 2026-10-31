## Two numbers on one line

If the input is on one line, such as `6 7`, `split_whitespace` splits the text at the spaces and each `next` gives the
following piece. `next` also needs `expect` because there may be no piece left.

```rust
use std::io;

fn main() {
    let mut line = String::new();
    io::stdin().read_line(&mut line).expect("could not read");

    let mut parts = line.split_whitespace();
    let a: i32 = parts.next().expect("first").parse().expect("not a number");
    let b: i32 = parts.next().expect("second").parse().expect("not a number");
    println!("{}", a * b);
}
```

With the input `6 7`:

```text
42
```

## All the input at once

`io::read_to_string` reads until the input ends. It is useful when you do not know how many lines will come:

```rust
use std::io;

fn main() {
    let text = io::read_to_string(io::stdin()).expect("could not read");
    println!("{}", text.lines().count());
    println!("{}", text.split_whitespace().count());
}
```

With two lines of input (`one two` and `three`):

```text
2
3
```

## When the input has ended

`read_line` also returns the number of bytes it read. If the input has ended it reads 0 bytes and the text stays empty:

```rust
use std::io;

fn main() {
    let mut line = String::new();
    io::stdin().read_line(&mut line).expect("could not read");
    println!("{}", line.len());
}
```

When no input is given:

```text
0
```

We will use this number to detect the end in a loop (Conditions and Loops).

## Common mistakes

| Symptom | Cause | Fix |
|---|---|---|
| `InvalidDigit` | `trim` forgotten, or the input is not a number | `line.trim().parse()` |
| `Empty` | The input is empty | Check the input |
| `E0284` | The target type is not written | `let n: i32 = ...` |
| `E0596` | `let line` is not `mut` | `let mut line` |
| The second number is wrong | `clear` forgotten | `line.clear();` |
| The question does not appear | `print!` is waiting | `io::stdout().flush()` |
