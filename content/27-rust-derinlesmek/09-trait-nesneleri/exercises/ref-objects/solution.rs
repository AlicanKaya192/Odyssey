trait Item {
    fn price(&self) -> u32;
}

struct Book {
    pages: u32,
}

struct Pen;

impl Item for Book {
    fn price(&self) -> u32 {
        self.pages / 10
    }
}

impl Item for Pen {
    fn price(&self) -> u32 {
        2
    }
}

fn total(items: &[&dyn Item]) -> u32 {
    items.iter().map(|i| i.price()).sum()
}

fn main() {
    println!("{}", total(&[&Book { pages: 100 }, &Pen]));
}
