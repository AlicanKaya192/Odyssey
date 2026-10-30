#[derive(Debug, PartialEq)]
enum Light {
    Red,
    Yellow,
    Green,
}

// impl Light { ... }

fn main() {
    println!("{:?}", Light::Red.next());
}
