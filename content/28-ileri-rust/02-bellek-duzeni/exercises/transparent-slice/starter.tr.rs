use std::slice;

struct Celsius(f64);

// fn as_numbers(list: &[Celsius]) -> &[f64] ...

fn main() {
    println!("{:?}", as_numbers(&[Celsius(1.5)]));
}
