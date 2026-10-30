trait Priced {
    fn price(&self) -> u32;
}

struct Apple;
struct Melon(u32);

impl Priced for Apple {
    fn price(&self) -> u32 {
        3
    }
}

impl Priced for Melon {
    fn price(&self) -> u32 {
        self.0 * 2
    }
}

// fn total ...

fn main() {
    println!("{}", total(&[Apple, Apple]));
    println!("{}", total(&[Melon(4)]));
}
