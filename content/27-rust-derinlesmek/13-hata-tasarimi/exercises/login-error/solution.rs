use std::fmt;

#[derive(Debug, PartialEq)]
enum LoginError {
    Empty,
    TooShort(usize),
}

impl fmt::Display for LoginError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            LoginError::Empty => write!(f, "password is empty"),
            LoginError::TooShort(n) => write!(f, "password has only {n} letters"),
        }
    }
}

impl std::error::Error for LoginError {}

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
