## A template

Copy and fill in:

```rust
use std::error::Error;
use std::fmt;
use std::num::ParseIntError;

#[derive(Debug)]
pub enum MyError {
    Parse(ParseIntError),
    Missing(String),
}

impl fmt::Display for MyError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            MyError::Parse(_) => write!(f, "bad number"),
            MyError::Missing(name) => write!(f, "{name} is missing"),
        }
    }
}

impl Error for MyError {
    fn source(&self) -> Option<&(dyn Error + 'static)> {
        match self {
            MyError::Parse(e) => Some(e),
            MyError::Missing(_) => None,
        }
    }
}

impl From<ParseIntError> for MyError {
    fn from(e: ParseIntError) -> Self {
        MyError::Parse(e)
    }
}

fn main() {
    let e = MyError::from("x".parse::<i32>().unwrap_err());
    println!("{e} / {}", e.source().is_some());
    println!("{}", MyError::Missing(String::from("port")));
}
```

## When writing the text

| Do | Do not |
|---|---|
| `cannot read port` | `Error: cannot read port!` |
| Lowercase, no period | A capital first letter, a period at the end |
| Write the input: `age 200 is too big` | `invalid input` |
| Put the cause in `source` | Also write the cause in the text |

It is lowercase with no period because the text may be added after another sentence: `error: cannot read port`.

## Review questions

| Question | If the answer is no |
|---|---|
| Would the caller do something different for this error? | Do not open a separate case; merge |
| Does the text say what is wrong? | Add the input |
| Is the cause carried without being lost? | Add `source` |
| Is it an expected case, or a program bug? | A program bug is a `panic!` |

## A public enum

In a library, adding a new error breaks the caller's `match`. `#[non_exhaustive]` prevents this:

```rust
#[non_exhaustive]
pub enum ParseError {
    Empty,
    TooLong,
}
```

A `match` outside the crate must now write a `_` arm; adding a new case breaks no one.
