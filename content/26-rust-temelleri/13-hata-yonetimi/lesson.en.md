# Error Handling

A file may not exist, a user may type a letter instead of a number, a network may drop. Programs meet errors. In many languages an error is thrown as an **exception**, and looking at a function's signature you cannot tell whether it may fail. Rust differs: a possible error is **written in the return type.**

## Two kinds of errors

| Kind | Example | In Rust |
|---|---|---|
| **Recoverable** | File missing, bad input | Return `Result` |
| **Unrecoverable** | A bug in the program, an array bound exceeded | `panic!` |

## Result

`Option` said "a value or nothing". `Result` says "success or failure":

```text
enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

`T` is the type of the value on success, `E` is the type of the error. Like `Option`, it comes automatically. Let us read a number:

```rust
fn main() {
    for text in ["42", "abc", ""] {
        match text.parse::<i32>() {
            Ok(n) => println!("number: {n}"),
            Err(e) => println!("error: {e}"),
        }
    }
}
```

```text
number: 42
error: invalid digit found in string
error: cannot parse integer from empty string
```

`parse` tries to turn text into a number. The error type is `ParseIntError`, which writes a readable message with `{}`. `match` forces you to handle both cases.

## Your own function

```rust
fn divide(a: i32, b: i32) -> Result<i32, String> {
    if b == 0 {
        return Err(String::from("division by zero"));
    }
    Ok(a / b)
}

fn main() {
    println!("{:?}", divide(10, 2));
    println!("{:?}", divide(1, 0));
}
```

```text
Ok(5)
Err("division by zero")
```

Anyone looking at the signature sees this function may fail. The caller **cannot ignore** the error, because it holds a `Result`, not an `i32`.

If you try to ignore it, the compiler warns:

```rust
fn save() -> Result<(), String> {
    Ok(())
}

fn main() {
    save();
    println!("done");
}
```

```text
warning: unused `Result` that must be used
 --> main.rs:6:5
  |
6 |     save();
  |     ^^^^^^
  |
  = note: this `Result` may be an `Err` variant, which should be handled
  = note: `#[warn(unused_must_use)]` (part of `#[warn(unused)]`) on by default
help: use `let _ = ...` to ignore the resulting value
  |
6 |     let _ = save();
  |     +++++++
```

This is a warning and the build does not stop, but since `#[must_use]` is written on it the compiler tells you that you ignored it.

## unwrap and expect

As with `Option`: on `Ok` they give the value, on `Err` they panic.

```rust
fn main() {
    let good: Result<i32, String> = Ok(3);
    println!("{}", good.unwrap());
    let bad: Result<i32, String> = Err(String::from("no value"));
    println!("{}", bad.expect("needed a value"));
}
```

```text
3

thread 'main' panicked at main.rs:5:24:
needed a value: "no value"
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

`expect` adds your own message at the start. Which one when?

| Place | Written |
|---|---|
| A small trial, sample code | `unwrap` |
| If you can say "this cannot happen" | `expect`, writing why |
| An error that can really happen | `match`, `?` or `unwrap_or` |

## Default values

```rust
fn main() {
    println!("{}", "7".parse::<i32>().unwrap_or(0));
    println!("{}", "x".parse::<i32>().unwrap_or(0));
    println!("{}", "x".parse::<i32>().unwrap_or_default());
    println!("{}", "x".parse::<i32>().is_err());
}
```

```text
7
0
0
true
```

## The ? operator

Passing an error upwards is very common. Written with `match` it gets long:

```rust
fn add_text(a: &str, b: &str) -> Result<i32, std::num::ParseIntError> {
    let x = match a.parse::<i32>() {
        Ok(n) => n,
        Err(e) => return Err(e),
    };
    let y = match b.parse::<i32>() {
        Ok(n) => n,
        Err(e) => return Err(e),
    };
    Ok(x + y)
}

fn main() {
    println!("{:?}", add_text("2", "3"));
    println!("{:?}", add_text("2", "x"));
}
```

```text
Ok(5)
Err(ParseIntError { kind: InvalidDigit })
```

`?` does the same with one character:

```rust
fn add_text(a: &str, b: &str) -> Result<i32, std::num::ParseIntError> {
    let x = a.parse::<i32>()?;
    let y = b.parse::<i32>()?;
    Ok(x + y)
}

fn main() {
    println!("{:?}", add_text("2", "3"));
    println!("{:?}", add_text("2", "x"));
}
```

```text
Ok(5)
Err(ParseIntError { kind: InvalidDigit })
```

<figure class="fig"><div class="flow"><span class="node">a.parse()?</span><span class="arrow">→</span><span class="node ok">If Ok, give the value</span><span class="arrow">→</span><span class="node no">If Err, return now</span></div><figcaption><code>?</code> either takes the value out or returns the error from the function.</figcaption></figure>

Several `?` can follow each other, and the code reads the "happy path" straight.

## ? only in a function returning Result

```rust
fn main() {
    let n = "21".parse::<i32>()?;
    println!("{n}");
}
```

```text
error[E0277]: the `?` operator can only be used in a function that returns `Result` or
`Option` (or another type that implements `FromResidual`)
 --> main.rs:2:32
  |
1 | fn main() {
  | --------- this function should return `Result` or `Option` to accept `?`
2 |     let n = "21".parse::<i32>()?;
  |                                ^ cannot use the `?` operator in a function that
  returns `()`
  |
help: consider adding return type
  |
1 ~ fn main() -> Result<(), Box<dyn std::error::Error>> {
2 |     let n = "21".parse::<i32>()?;
3 |     println!("{n}");
4 +     Ok(())
  |
```

If the function does not return `Result`, where would it return the error to? `main` can return `Result` too:

```rust
fn main() -> Result<(), std::num::ParseIntError> {
    let n = "21".parse::<i32>()?;
    println!("{}", n * 2);
    Ok(())
}
```

```text
42
```

If `main` returns `Err`, the program writes the error and exits with 1:

```rust
fn main() -> Result<(), String> {
    println!("start");
    Err(String::from("config is missing"))
}
```

```text
start
Error: "config is missing"
```

## If the error type differs

`?` wants the error types to match:

```rust
fn read(text: &str) -> Result<i32, String> {
    let n = text.parse::<i32>()?;
    Ok(n)
}

fn main() {
    println!("{:?}", read("1"));
}
```

```text
error[E0277]: `?` couldn't convert the error to `String`
 --> main.rs:2:32
  |
1 | fn read(text: &str) -> Result<i32, String> {
  |                        ------------------- expected `String` because of this
2 |     let n = text.parse::<i32>()?;
  |                  --------------^ the trait `From<ParseIntError>` is not implemented
  for `String`
  |                  |
  |                  this can't be annotated with `?` because it has type `Result<_,
  ParseIntError>`
  |
  = note: the question mark operation (`?`) implicitly performs a conversion on the
    error value using the `From` trait
  = help: `String` implements trait `From<T>`:
            From<&String>
            From<&mut str>
            From<&str>
            From<Box<str>>
            From<Cow<'_, str>>
            From<char>
```

For now the simplest way is `map_err`: it turns the error into our type. The `|e| ...` inside the parentheses is a nameless one-line function:

```rust
fn double(text: &str) -> Result<i32, String> {
    let n = text.parse::<i32>().map_err(|e| format!("bad number {text:?}: {e}"))?;
    Ok(n * 2)
}

fn main() {
    println!("{:?}", double("4"));
    println!("{:?}", double("x"));
}
```

```text
Ok(8)
Err("bad number \"x\": invalid digit found in string")
```

## Your own error type

A `String` error is enough, but the caller cannot act on the kind of error. An enum is exactly for this:

```rust
#[derive(Debug)]
enum AgeError {
    NotANumber,
    OutOfRange(i32),
}

fn read_age(text: &str) -> Result<i32, AgeError> {
    let age = text.parse::<i32>().map_err(|_| AgeError::NotANumber)?;
    if age < 0 || age > 150 {
        return Err(AgeError::OutOfRange(age));
    }
    Ok(age)
}

fn main() {
    for text in ["36", "x", "200"] {
        match read_age(text) {
            Ok(age) => println!("age {age}"),
            Err(AgeError::NotANumber) => println!("not a number"),
            Err(AgeError::OutOfRange(n)) => println!("{n} is out of range"),
        }
    }
}
```

```text
age 36
not a number
200 is out of range
```

The caller can now handle each error separately with `match`, and when a new error kind is added the compiler shows the missing arm. In the next module we will complete this type with the `Display` and `Error` traits.

## Between Option and Result

```rust
fn first_char(text: &str) -> Result<char, String> {
    text.chars().next().ok_or(String::from("empty"))
}

fn first_number(list: &[&str]) -> Option<i32> {
    let text = list.first()?;
    text.parse().ok()
}

fn main() {
    println!("{:?} {:?}", first_char("hi"), first_char(""));
    println!("{:?}", first_number(&["7"]));
    println!("{:?} {:?}", first_number(&["x"]), first_number(&[]));
}
```

```text
Ok('h') Err("empty")
Some(7)
None None
```

`ok_or` turns an `Option` into a `Result`, and `.ok()` turns a `Result` into an `Option`. `?` also works on an `Option` in a function returning `Option`.

## When panic!?

`panic!` stops the program. It is used **when there is a bug in the program**, not because of a person's input:

```rust
fn main() {
    let level = 9;
    if level > 5 {
        panic!("level must be at most 5, got {level}");
    }
}
```

```text
thread 'main' panicked at main.rs:4:9:
level must be at most 5, got 9
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

This output goes to stderr and the program exits with 101. The rule: if the problem is something the caller can fix, `Result`; if it is the code's own bug, `panic!`.

## Summary

- A possible error is written in the return type: `Result<T, E>`.
- `Ok(value)` and `Err(error)` are the two cases. `match` wants both.
- `unwrap` and `expect` panic on `Err`; do not use them for real errors.
- `?` passes the error upwards; it works only in a function returning `Result` (or `Option`).
- If types differ, `map_err`. If the caller will tell errors apart, an enum error type.
- `panic!` only for the program's own bugs.
