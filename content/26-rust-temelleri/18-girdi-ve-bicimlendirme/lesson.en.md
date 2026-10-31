# Input and Formatting

So far every value has lived inside the code. A real program takes data from outside and writes the result in a readable
form. This section teaches both: reading a line from the user, turning it into a number, and writing output aligned and
with as many digits as you want.

## Reading a line

```rust
use std::io;

fn main() {
    let mut line = String::new();
    io::stdin().read_line(&mut line).expect("could not read");
    println!("You wrote: {line}");
}
```

Input:

```text
Ada
```

Output:

```text
You wrote: Ada
```

There is a lot that is new in this code. You do not need to understand it all now; most of it gets its own section
later. For now write these lines as a **pattern**:

<figure class="fig"><div class="anat"><div class="anat-row"><span><code>use std::io;</code></span><span>I will use the input and output tools under the name <code>io</code>.</span></div><div class="anat-row"><span><code>String::new()</code></span><span>Makes an empty text that can grow.</span></div><div class="anat-row"><span><code>io::stdin()</code></span><span><b>Standard input</b> (stdin): data coming into the program from outside, usually the keyboard.</span></div><div class="anat-row"><span><code>.read_line(&amp;mut line)</code></span><span>Reads a line and adds it to the end of the text <code>line</code>. <code>&amp;mut</code> means "you may change this"; we will see it in the Borrowing section.</span></div><div class="anat-row"><span><code>.expect("...")</code></span><span>If reading fails, stops the program with this message.</span></div></div><figcaption>The parts of the input pattern.</figcaption></figure>

In Odyssey, exercises that need input get it ready-made from the checker; it does not wait for you to type. If you run it
on your own computer, the program waits for you to type a line.

## The invisible line ending

The text `line` holds something you cannot see: pressing Enter is part of the input too, and it goes into the text.
The `{:?}` format writes text in quotes and shows invisible characters:

```rust
use std::io;

fn main() {
    let mut line = String::new();
    io::stdin().read_line(&mut line).expect("could not read");
    println!("{line:?}");
}
```

```text
"Ada\r\n"
```

`\r\n` is the line ending on Windows (on Linux and macOS it is just `\n`). `trim` removes spaces and the line ending at both
ends. It leaves spaces in the middle alone:

```rust
use std::io;

fn main() {
    let mut line = String::new();
    io::stdin().read_line(&mut line).expect("could not read");
    let name = line.trim();
    println!("Hello, {name}!");
}
```

```text
Hello, Ada!
```

The input here was `  Ada  `.

## From text to number: `parse`

`read_line` always gives text. Even if `41` is typed, what we have is the text `"41\r\n"`, and you cannot add with it.
`parse` tries to turn text into a number:

```rust
use std::io;

fn main() {
    let mut line = String::new();
    io::stdin().read_line(&mut line).expect("could not read");
    let age: i32 = line.trim().parse().expect("not a number");
    println!("{}", age + 1);
}
```

```text
42
```

Notice two things. `: i32` says which type to convert to; if you leave it out the compiler asks:

```rust
use std::io;

fn main() {
    let mut line = String::new();
    io::stdin().read_line(&mut line).expect("could not read");
    let age = line.trim().parse().expect("not a number");
    println!("{age}");
}
```

```text
error[E0284]: type annotations needed
 --> main.rs:6:9
  |
6 |     let age = line.trim().parse().expect("not a number");
  |         ^^^               ----- type must be known at this point
  |
  = note: cannot satisfy `<_ as FromStr>::Err == _`
  = note: the type must also implement `FromStr`
note: required by a bound in `core::str::<impl str>::parse`
help: consider giving `age` an explicit type
  |
6 |     let age: /* Type */ = line.trim().parse().expect("not a number");
  |            ++++++++++++
```

The second is `trim`. A line ending is not a digit, so without it the conversion fails and `expect` stops the program:

```rust
use std::io;

fn main() {
    let mut line = String::new();
    io::stdin().read_line(&mut line).expect("could not read");
    let age: i32 = line.parse().expect("not a number");
    println!("{}", age + 1);
}
```

```text
thread 'main' panicked at main.rs:6:33:
not a number: ParseIntError { kind: InvalidDigit }
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

The same happens if the user types `abc`. Stopping is enough for now; handling the error gently comes in the Error
Handling section.

## Asking on the same line

`println!` adds a line ending, `print!` does not. But the text of `print!` can wait until a line ending comes, so the
program starts waiting for input before the question is on the screen. `flush` sends what is waiting right away:

```rust
use std::io::{self, Write};

fn main() {
    print!("What is your name? ");
    io::stdout().flush().expect("could not write");

    let mut line = String::new();
    io::stdin().read_line(&mut line).expect("could not read");
    println!("Hello, {}!", line.trim());
}
```

With the input `Ada`:

```text
What is your name? Hello, Ada!
```

In your own terminal the name you type also appears on that line, and Enter moves to a new one. Here the input is
redirected, so what you typed does not show. `use std::io::{self, Write};` also brings in `Write`, for `flush`.

## Reading two lines: the `clear` trap

`read_line` does **not overwrite** the text, **it adds to the end**. If you read twice with the same text, the two lines
sit side by side:

```rust
use std::io;

fn main() {
    let mut line = String::new();
    io::stdin().read_line(&mut line).expect("could not read");
    io::stdin().read_line(&mut line).expect("could not read");
    println!("{line:?}");
}
```

With the inputs `3` and `4`:

```text
"3\r\n4\r\n"
```

This text cannot become a number. Empty the text before the second read:

```rust
use std::io;

fn main() {
    let mut line = String::new();
    io::stdin().read_line(&mut line).expect("could not read");
    let a: i32 = line.trim().parse().expect("not a number");

    line.clear();
    io::stdin().read_line(&mut line).expect("could not read");
    let b: i32 = line.trim().parse().expect("not a number");

    println!("{}", a + b);
}
```

```text
7
```

## Putting a value in its place

`println!`, `format!` and friends share one format language. A pair of curly braces marks where a value goes:

```rust
fn main() {
    let name = "Ada";
    let age = 36;
    println!("{} is {}", name, age);
    println!("{name} is {age}");
    println!("{0} and {1} and {0}", name, age);
    println!("{who} is {}", age + 1, who = name);
}
```

```text
Ada is 36
Ada is 36
Ada and 36 and Ada
Ada is 37
```

Writing the name inside the braces reads best. But only a plain variable name fits: `{age + 1}` does not work, and a
calculation goes after the comma.

## Decimal places

What comes after `:` states the format. `.2` means 2 digits after the point:

```rust
fn main() {
    let pi = 3.14159;
    println!("{pi:.2}");
    println!("{:.0}", pi);
    println!("{:.3}", 2.0);
    println!("{:.0}", 2.5);
    println!("{:.0}", 3.5);
}
```

```text
3.14
3
2.000
2
4
```

It does not change the number, only how it is written. Look at the last two lines: `2.5` became `2` and `3.5` became `4`. A
value exactly in the middle rounds to its even neighbour, not always upwards.

## Width and alignment

When writing columns, each value gets a fixed width. The square brackets are there so that we can see the edges:

```rust
fn main() {
    println!("[{:5}]", 42);
    println!("[{:5}]", "ab");
    println!("[{:>5}]", "ab");
    println!("[{:<5}]", 42);
    println!("[{:^5}]", "ab");
    println!("[{:*^7}]", "ab");
    println!("[{:05}]", 42);
    println!("[{:+}]", 42);
}
```

```text
[   42]
[ab   ]
[   ab]
[42   ]
[ ab  ]
[**ab***]
[00042]
[+42]
```

| Format | Meaning |
|---|---|
| `{:5}` | 5 characters; numbers align right, text left |
| `{:>5}` | Align right |
| `{:<5}` | Align left |
| `{:^5}` | Centre; if it does not divide evenly the extra goes right |
| `{:*^7}` | Fill with `*` instead of spaces |
| `{:05}` | Fill with zeros instead of spaces |
| `{:+}` | Also write the plus sign |

Combine these and you get a table. `{:>8.2}`: width 8, aligned right, 2 digits:

```rust
fn main() {
    println!("{:<8}{:>4}{:>8}", "item", "qty", "price");
    println!("{:<8}{:>4}{:>8.2}", "tea", 2, 3.5);
    println!("{:<8}{:>4}{:>8.2}", "coffee", 1, 12.25);
}
```

```text
item     qty   price
tea        2    3.50
coffee     1   12.25
```

## Other notations

You can write the same number in another base. `{:?}` is the notation meant for developers: it writes text in quotes and
also handles types that `{}` does not accept, such as tuples. `{:#?}` does the same over several lines.

```rust
fn main() {
    println!("{:b}", 10);
    println!("{:o}", 10);
    println!("{:x}", 255);
    println!("{:X}", 255);
    println!("{:#x}", 255);
    println!("{:08b}", 10);
    println!("{:e}", 1500.0);
}
```

```text
1010
12
ff
FF
0xff
00001010
1.5e3
```

```rust
fn main() {
    let name = "Ada";
    println!("{name}");
    println!("{name:?}");
    let point = (3, "north");
    println!("{point:?}");
    println!("{point:#?}");
}
```

```text
Ada
"Ada"
(3, "north")
(
    3,
    "north",
)
```

## Writing a format into text

`format!` is written like `println!` but gives a `String` instead of printing. To write a curly brace itself, write it twice:

```rust
fn main() {
    let price = 12.5;
    let label = format!("{price:.2} TL");
    println!("{label}");
    println!("{}", label.len());
    println!("{{not a placeholder}}");
}
```

```text
12.50 TL
8
{not a placeholder}
```

## Summary

- The pattern for reading a line: `String::new()`, `io::stdin().read_line(&mut line).expect("...")`.
- The text read ends with a line ending; `trim` removes it. `{:?}` shows what is invisible.
- `line.trim().parse()` converts to a number; the target type is stated with `: i32`, and it can fail.
- `read_line` adds to the end: call `line.clear()` before reading again.
- `{:.2}` digits, `{:>5}` alignment and width, `{:05}` zero fill; together `{:>8.2}`.
- `format!` makes a `String` with the same format; `{:?}` and `{:#?}` are developer notation.
