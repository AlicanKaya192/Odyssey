struct Bag {
    items: Vec<i32>,
}

// impl IntoIterator ...

fn main() {
    let bag = Bag { items: vec![1, 2] };
    let mut total = 0;
    for x in &bag {
        total += x;
    }
    println!("{total} {}", bag.items.len());
}
