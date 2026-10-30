struct Bag {
    items: Vec<i32>,
}

impl<'a> IntoIterator for &'a Bag {
    type Item = &'a i32;
    type IntoIter = std::slice::Iter<'a, i32>;

    fn into_iter(self) -> Self::IntoIter {
        self.items.iter()
    }
}

fn main() {
    let bag = Bag { items: vec![1, 2] };
    let mut total = 0;
    for x in &bag {
        total += x;
    }
    println!("{total} {}", bag.items.len());
}
