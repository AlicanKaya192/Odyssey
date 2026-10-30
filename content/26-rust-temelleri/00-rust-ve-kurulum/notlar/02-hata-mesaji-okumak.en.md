While learning Rust, the compiler's messages are where you will spend most of your time. They all follow the same pattern.

```rust
fn main() {
    println!("{} and {}", 1);
}
```

```text
error: 2 positional arguments in format string, but there is 1 argument
 --> main.rs:2:15
  |
2 |     println!("{} and {}", 1);
  |               ^^     ^^   -
```

## The parts

| Part | Meaning |
|---|---|
| `error` | No program was produced; you need to fix it |
| `warning` | A program was produced, but the compiler found something odd |
| A code such as `[E0599]` | The error's identity |
| `-->` | File, line, column |
| `^^^^` | The part at fault |
| `note:` | Extra explanation |
| `help:` | A suggested fix |

## Opening an error code

If an error has a code in square brackets, the compiler can give a longer explanation of it. Type this in a terminal:

```bash
rustc --explain E0599
```

The output explains the error with an example and needs no internet.

## A good habit

1. Read only the first error.
2. Go to the place on the `-->` line.
3. If there is a `help:`, try that first.
4. Compile again; the number of errors often drops at once.

Read the warnings too. Even when the program runs, a warning often points at a real oversight,
such as a variable you never used.
