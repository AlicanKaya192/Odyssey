#[derive(Debug, PartialEq)]
enum AgeError {
    NotANumber,
    OutOfRange(i32),
}

// fn read_age ...

fn main() {
    println!("{:?}", read_age("36"));
}
