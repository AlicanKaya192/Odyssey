# Designing Errors

In the Fundamentals we learned `Result` and the `?` operator. Now the question is different: **What should the error's type be?** If the error is a single `String`, the calling code can only print it. It cannot look at what happened and decide. A well designed error type gives the caller a choice.

## An error is an enum

Write the possible errors one by one. Two traits make it a real error:

- `Display`: The text a person reads.
- `std::error::Error`: It says "this type is an error". Its body can be empty, because it requires `Debug` and `Display`, and the rest has a ready form.

```rust
use std::fmt;

#[derive(Debug)]
enum AgeError {
    Empty,
    TooBig(u32),
}

impl fmt::Display for AgeError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            AgeError::Empty => write!(f, "age is empty"),
            AgeError::TooBig(n) => write!(f, "age {n} is too big"),
        }
    }
}

impl std::error::Error for AgeError {}

fn check(age: Option<u32>) -> Result<u32, AgeError> {
    let age = age.ok_or(AgeError::Empty)?;
    if age > 150 {
        return Err(AgeError::TooBig(age));
    }
    Ok(age)
}

fn main() {
    println!("{:?}", check(Some(30)));
    for input in [None, Some(200)] {
        if let Err(e) = check(input) {
            println!("{e} / {e:?}");
        }
    }
}
```

```text
Ok(30)
age is empty / Empty
age 200 is too big / TooBig(200)
```

`{e}` is for the user, `{e:?}` for the developer. Because the error is a type, the caller can handle each case separately with `match`.

## `?` and From

`?` does not return the error as it is; it first converts it with `From`. If no conversion is written:

```rust
use std::num::ParseIntError;

#[derive(Debug)]
enum AppError {
    Parse(ParseIntError),
    Negative(i64),
}

fn read_age(text: &str) -> Result<i64, AppError> {
    let n = text.trim().parse::<i64>()?;
    if n < 0 {
        return Err(AppError::Negative(n));
    }
    Ok(n)
}

fn main() {
    println!("{:?}", read_age("30"));
    println!("{:?}", read_age("x"));
    println!("{:?}", read_age("-1"));
}
```

```text
error[E0277]: `?` couldn't convert the error to `AppError`
  --> main.rs:10:39
   |
 9 | fn read_age(text: &str) -> Result<i64, AppError> {
   |                            --------------------- expected `AppError` because of
   this
10 |     let n = text.trim().parse::<i64>()?;
   |                         --------------^ the trait `From<ParseIntError>` is not
   implemented for `AppError`
   |                         |
   |                         this can't be annotated with `?` because it has type
   `Result<_, ParseIntError>`
   |
note: `AppError` needs to implement `From<ParseIntError>`
  --> main.rs:4:1
   |
 4 | enum AppError {
   | ^^^^^^^^^^^^^
   = note: the question mark operation (`?`) implicitly performs a conversion on the
     error value using the `From` trait
```

The compiler says exactly this: `?` cannot convert `ParseIntError` to `AppError`. Once `From` is written, every `?` converts by itself:

```rust
use std::num::ParseIntError;

#[derive(Debug)]
enum AppError {
    Parse(ParseIntError),
    Negative(i64),
}

impl From<ParseIntError> for AppError {
    fn from(e: ParseIntError) -> Self {
        AppError::Parse(e)
    }
}

fn read_age(text: &str) -> Result<i64, AppError> {
    let n = text.trim().parse::<i64>()?;
    if n < 0 {
        return Err(AppError::Negative(n));
    }
    Ok(n)
}

fn main() {
    println!("{:?}", read_age("30"));
    println!("{:?}", read_age("x"));
    println!("{:?}", read_age("-1"));
}
```

```text
Ok(30)
Err(Parse(ParseIntError { kind: InvalidDigit }))
Err(Negative(-1))
```

No conversion is written in the function's body. This is how the clutter of `map_err` ends.

## The error's cause

One error is born from another: "the port could not be read" because "the number is too large". The `source` method of the `Error` trait builds this chain. The upper layer adds **context**, and the lower keeps the **cause**:

```rust
use std::error::Error;
use std::fmt;
use std::num::ParseIntError;

#[derive(Debug)]
struct ConfigError {
    key: String,
    source: ParseIntError,
}

impl fmt::Display for ConfigError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "bad value for {}", self.key)
    }
}

impl Error for ConfigError {
    fn source(&self) -> Option<&(dyn Error + 'static)> {
        Some(&self.source)
    }
}

fn read_port(text: &str) -> Result<u16, ConfigError> {
    text.parse::<u16>().map_err(|e| ConfigError {
        key: String::from("port"),
        source: e,
    })
}

fn report(err: &dyn Error) {
    println!("error: {err}");
    let mut current = err.source();
    while let Some(cause) = current {
        println!("caused by: {cause}");
        current = cause.source();
    }
}

fn main() {
    if let Err(e) = read_port("99999") {
        report(&e);
    }
}
```

```text
error: bad value for port
caused by: number too large to fit in target type
```

Do not let the `dyn Error + 'static` inside `source` scare you: it means "any error". The `report` function walking the chain works with any error type, because it knows only the trait.

One rule: do not write the cause and the text twice. `Display` says its own sentence, and `source` carries the cause. If both write the same thing, the text appears twice when the chain is printed.

## A short name

If the same error type is written in every function, define a short name. The standard library does this too (`std::io::Result`, `fmt::Result`):

```rust
#[derive(Debug)]
enum AppError {
    Empty,
}

type Result<T> = std::result::Result<T, AppError>;

fn first(list: &[i32]) -> Result<i32> {
    list.first().copied().ok_or(AppError::Empty)
}

fn main() {
    println!("{:?}", first(&[4, 5]));
    println!("{:?}", first(&[]));
}
```

```text
Ok(4)
Err(Empty)
```

## Box&lt;dyn Error&gt;: a box taking any error

In a small tool, writing an enum may be too much. `Box<dyn Error>` takes any error type, and `?` does the conversion itself. Plain text also becomes an error with `.into()`:

```rust
use std::error::Error;

fn sum_line(text: &str) -> Result<i32, Box<dyn Error>> {
    if text.is_empty() {
        return Err("empty line".into());
    }
    let mut total = 0;
    for part in text.split(',') {
        total += part.trim().parse::<i32>()?;
    }
    Ok(total)
}

fn main() {
    for line in ["1, 2", "", "1, x"] {
        match sum_line(line) {
            Ok(n) => println!("{n}"),
            Err(e) => println!("error: {e}"),
        }
    }
}
```

```text
3
error: empty line
error: invalid digit found in string
```

The price: the caller no longer knows what happened, and can only print the text. If you really need to look, `downcast_ref` asks about the type at run time:

```rust
use std::num::ParseIntError;

fn main() {
    let err = sum_line("x").unwrap_err();
    if let Some(p) = err.downcast_ref::<ParseIntError>() {
        println!("number problem: {p}");
    }
    println!("{}", err.is::<std::fmt::Error>());
}
```

```text
number problem: invalid digit found in string
false
```

If `downcast_ref` is proving useful, it is time to make the error type an enum.

## Which one?

| You are writing | Choose | Why |
|---|---|---|
| A library | Your own enum | The caller decides by case |
| An application, a small tool | `Box<dyn Error>` | The error is finally printed |
| A recoverable error in an application | An enum | `match` to retry or fall back to a default |

## Returning an error from main

`main` can return a `Result` too. The problem: it writes the error with `Debug`, not `Display`.

```rust
use std::error::Error;

fn main() -> Result<(), Box<dyn Error>> {
    let n: i32 = "x".parse()?;
    println!("{n}");
    Ok(())
}
```

```text
Error: ParseIntError { kind: InvalidDigit }
```

We do not want to show the user this. Put the real work in a function called `run`; let `main` write the error properly and choose the exit code:

```rust
use std::num::ParseIntError;
use std::process::ExitCode;

fn run() -> Result<i32, ParseIntError> {
    "x".parse()
}

fn main() -> ExitCode {
    match run() {
        Ok(n) => {
            println!("{n}");
            ExitCode::SUCCESS
        }
        Err(e) => {
            eprintln!("error: {e}");
            ExitCode::from(2)
        }
    }
}
```

```text
error: invalid digit found in string
```

## Many Results

While converting a list, each item produces a `Result`. `collect` can gather these into one `Result`, stopping at the first error; to see all errors, `partition`:

```rust
fn main() {
    let good: Result<Vec<i32>, _> = ["1", "2"].iter().map(|s| s.parse::<i32>()).collect();
    let bad: Result<Vec<i32>, _> = ["1", "x"].iter().map(|s| s.parse::<i32>()).collect();
    println!("{good:?}");
    println!("{bad:?}");

    let (ok, err): (Vec<_>, Vec<_>) = ["1", "x", "3"]
        .iter()
        .map(|s| s.parse::<i32>())
        .partition(|r| r.is_ok());
    println!("{} {}", ok.len(), err.len());
}
```

```text
Ok([1, 2])
Err(ParseIntError { kind: InvalidDigit })
2 1
```

## Summary

- An error is an enum: `Debug`, `Display`, `std::error::Error`.
- Once `From` is written, `?` converts by itself.
- `source` carries the cause, and `Display` says its own sentence.
- An enum in a library, `Box<dyn Error>` in a small application.
- An error returned from `main` is written with `Debug`; for proper output, `run` and `ExitCode`.
