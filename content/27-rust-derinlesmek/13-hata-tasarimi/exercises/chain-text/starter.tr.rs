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

// impl Error for FieldError ...

fn read_field(name: &str, text: &str) -> Result<i32, FieldError> {
    text.parse().map_err(|e| FieldError {
        field: name.to_string(),
        cause: e,
    })
}

// fn chain_text(err: &dyn Error) -> String ...

fn main() {
    let e = read_field("age", "x").unwrap_err();
    println!("{}", chain_text(&e));
}
