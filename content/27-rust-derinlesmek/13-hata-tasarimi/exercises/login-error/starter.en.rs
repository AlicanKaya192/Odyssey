use std::fmt;

#[derive(Debug, PartialEq)]
enum LoginError {
    Empty,
    TooShort(usize),
}

// impl fmt::Display for LoginError ...
// impl std::error::Error for LoginError {}

fn check_password(text: &str) -> Result<(), LoginError> {
    if text.is_empty() {
        return Err(LoginError::Empty);
    }
    if text.len() < 8 {
        return Err(LoginError::TooShort(text.len()));
    }
    Ok(())
}

fn main() {
    if let Err(e) = check_password("abc") {
        println!("{e}");
    }
}
