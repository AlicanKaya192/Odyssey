use std::str::FromStr;

#[derive(Debug, PartialEq)]
struct Rgb {
    r: u8,
    g: u8,
    b: u8,
}

// impl FromStr ...

fn main() {
    println!("{:?}", "1,2,3".parse::<Rgb>());
}
