A program can take data from outside. The simplest way is to read one line from **standard input**.

```rust
fn main() {
    let mut line = String::new();
    std::io::stdin().read_line(&mut line).expect("read failed");
    let name = line.trim();
    println!("Hello, {name}!");
}
```

With `Ada` as input:

```text
Hello, Ada!
```

Line by line:

| Code | Meaning |
|---|---|
| `String::new()` | Opens an empty text that can grow |
| `std::io::stdin()` | Standard input: the keyboard or redirected data |
| `.read_line(&mut line)` | Appends one line to the text `line` |
| `.expect("...")` | Stops with this message if reading fails |
| `.trim()` | Removes spaces at the start and end, and the line ending |

`&mut line` says "I lend you line so that you can change it". We will see this in section seven. For now write it as a pattern.

## Turning text into a number

```rust
fn main() {
    let mut line = String::new();
    std::io::stdin().read_line(&mut line).expect("read failed");
    let n: i32 = line.trim().parse().expect("not a number");
    println!("{}", n * 2);
}
```

With `21` as input:

```text
42
```

`.parse()` tries to turn text into a number. `: i32` says which type to turn it into. It can fail (the text may be `abc`), so `.expect` is needed. We will
learn to handle errors gently in section thirteen.

## In this path

In exercises that want input, Odyssey gives your program prepared input. It does not wait for you to type like a user.
