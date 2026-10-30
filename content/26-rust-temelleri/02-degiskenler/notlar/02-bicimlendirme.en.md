`println!` does more than put values into text. After a colon you can write a format.

```rust
fn main() {
    let pi = 3.14159;
    let n = 7;
    println!("[{:.2}]", pi);
    println!("[{:>6}]", n);
    println!("[{:<6}]", n);
    println!("[{:^6}]", n);
    println!("[{:03}]", n);
    println!("{0} {0} {1}", n, pi);
    println!("{{{n}}}");
}
```

```text
[3.14]
[     7]
[7     ]
[  7   ]
[007]
7 7 3.14159
{7}
```

## Card

| Written | Result | What it does |
|---|---|---|
| `{x}` | the value | Writes the variable directly |
| `{0} {0}` | twice | Refers to the same value by position |
| `{:.2}` | `3.14` | Two digits after the decimal point |
| `{:>6}` | right aligned | In a width of 6 characters |
| `{:<6}` | left aligned | In a width of 6 characters |
| `{:^6}` | centred | In a width of 6 characters |
| `{:03}` | `007` | Pads the start with zeros |
| `{:?}` | debug | Shows the value for a programmer |

`{:?}` will be very useful later: it prints lists and structures directly. Plain `{}` does not accept them.

## A brace itself

To write a real brace in text, write it twice: `{{` and `}}`.

## print!, eprintln!

| Macro | What it does |
|---|---|
| `println!` | Writes and moves to the next line |
| `print!` | Writes without moving to the next line |
| `eprintln!` | Writes to the error channel |
| `format!` | Does not write; gives the text back |

`eprintln!` is for error messages. Even if the program's output is redirected to a file, the error message stays on the screen.
