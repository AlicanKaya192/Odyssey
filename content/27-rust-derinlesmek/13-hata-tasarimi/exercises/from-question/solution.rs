use std::num::ParseIntError;

#[derive(Debug, PartialEq)]
enum OrderError {
    Parse(ParseIntError),
    Zero,
}

impl From<ParseIntError> for OrderError {
    fn from(e: ParseIntError) -> Self {
        OrderError::Parse(e)
    }
}

fn read_quantity(text: &str) -> Result<u32, OrderError> {
    let n: u32 = text.parse()?;
    if n == 0 {
        return Err(OrderError::Zero);
    }
    Ok(n)
}

fn main() {
    println!("{:?}", read_quantity("3"));
}
