#[derive(Debug, PartialEq)]
enum ParseError {
    Empty,
    NotNumber,
}

fn read_number(text: &str) -> Result<i32, ParseError> {
    if text.is_empty() {
        return Err(ParseError::Empty);
    }
    text.parse().map_err(|_| ParseError::NotNumber)
}

// fn is_empty_error ...

fn main() {
    println!("{}", is_empty_error(""));
}
