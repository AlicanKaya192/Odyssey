We saw how to read input in the Input and Formatting section. Combined with a loop, a program can keep running until the
user stops typing.

## Until the input ends

```rust
use std::io;

fn main() {
    let mut total = 0;
    let mut line = String::new();
    loop {
        line.clear();
        let bytes = io::stdin().read_line(&mut line).expect("could not read");
        if bytes == 0 || line.trim() == "end" {
            break;
        }
        let n: i32 = line.trim().parse().expect("not a number");
        total += n;
    }
    println!("total: {total}");
}
```

With the input lines `4`, `5`, `end`, `7`:

```text
total: 9
```

| Line | Why |
|---|---|
| `line.clear()` | `read_line` adds to the end; each round starts afresh |
| `let bytes = ...` | `read_line` gives the number of bytes read |
| `bytes == 0` | The input ended: 0 bytes were read |
| `line.trim() == "end"` | The user wants to finish |

The `7` after `end` was never read, because the loop ended there.

## A small game

`if`, `else if` and `break` together make a guessing game:

```rust
use std::io;

fn main() {
    let secret = 7;
    let mut line = String::new();
    loop {
        line.clear();
        let bytes = io::stdin().read_line(&mut line).expect("could not read");
        if bytes == 0 {
            println!("no more input");
            break;
        }
        let guess: i32 = line.trim().parse().expect("not a number");
        if guess < secret {
            println!("{guess}: too low");
        } else if guess > secret {
            println!("{guess}: too high");
        } else {
            println!("{guess}: found");
            break;
        }
    }
}
```

With the input lines `3`, `9`, `7`, `1`:

```text
3: too low
9: too high
7: found
```

## In this path

In exercises that need input, Odyssey hands the program ready-made input. It does not wait for you to type like a user.
