trait Converter {
    type Output;

    fn convert(&self, input: &str) -> Option<Self::Output>;
}

struct ToInt;
struct ToUpper;

impl Converter for ToInt {
    type Output = i32;

    fn convert(&self, input: &str) -> Option<i32> {
        input.parse().ok()
    }
}

impl Converter for ToUpper {
    type Output = String;

    fn convert(&self, input: &str) -> Option<String> {
        if input.is_empty() {
            return None;
        }
        Some(input.to_uppercase())
    }
}

fn main() {
    println!("{:?}", ToInt.convert("5"));
    println!("{:?}", ToUpper.convert("hi"));
}
