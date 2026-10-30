fn main() -> Result<(), std::num::ParseIntError> {
    let n = "21".parse::<i32>()?;
    println!("{}", n * 2);
    Ok(())
}
