#[derive(Debug, PartialEq)]
enum AgeError {
    NotANumber,
    OutOfRange(i32),
}

fn read_age(text: &str) -> Result<i32, AgeError> {
    let age = text.parse::<i32>().map_err(|_| AgeError::NotANumber)?;
    if age < 0 || age > 150 {
        return Err(AgeError::OutOfRange(age));
    }
    Ok(age)
}

fn main() {
    println!("{:?}", read_age("36"));
}
