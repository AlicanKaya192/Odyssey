use std::error::Error;

// fn total_of(text: &str) -> Result<i32, Box<dyn Error>> ...

fn main() {
    println!("{:?}", total_of("1 2 3").unwrap());
}
