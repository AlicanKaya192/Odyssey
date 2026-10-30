use std::error::Error;
use std::fmt;
use std::num::ParseIntError;

#[derive(Debug)]
struct FieldError {
    field: String,
    cause: ParseIntError,
}

impl fmt::Display for FieldError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "bad field {}", self.field)
    }
}

impl Error for FieldError {
    fn source(&self) -> Option<&(dyn Error + 'static)> {
        Some(&self.cause)
    }
}

fn read_field(name: &str, text: &str) -> Result<i32, FieldError> {
    text.parse().map_err(|e| FieldError {
        field: name.to_string(),
        cause: e,
    })
}

fn chain_text(err: &dyn Error) -> String {
    let mut text = err.to_string();
    let mut current = err.source();
    while let Some(cause) = current {
        text.push_str(" -> ");
        text.push_str(&cause.to_string());
        current = cause.source();
    }
    text
}

fn main() {
    let e = read_field("age", "x").unwrap_err();
    println!("{}", chain_text(&e));
}
