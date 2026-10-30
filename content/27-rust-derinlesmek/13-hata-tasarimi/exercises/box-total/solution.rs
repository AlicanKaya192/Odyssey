use std::error::Error;

fn total_of(text: &str) -> Result<i32, Box<dyn Error>> {
    if text.trim().is_empty() {
        return Err("nothing to add".into());
    }
    let mut total = 0;
    for part in text.split_whitespace() {
        total += part.parse::<i32>()?;
    }
    Ok(total)
}

fn main() {
    println!("{:?}", total_of("1 2 3").unwrap());
}
