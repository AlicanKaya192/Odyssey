use std::num::ParseIntError;

#[derive(Debug, PartialEq)]
enum OrderError {
    Parse(ParseIntError),
    Zero,
}

// impl From<ParseIntError> for OrderError ...

// fn read_quantity(text: &str) -> Result<u32, OrderError> ...

fn main() {
    println!("{:?}", read_quantity("3"));
}
