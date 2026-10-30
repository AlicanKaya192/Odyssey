struct Windows2<'a, T> {
    items: &'a [T],
    index: usize,
}

// impl Iterator ...

fn main() {
    let list = [1, 2, 3];
    for w in (Windows2 { items: &list, index: 0 }) {
        println!("{:?}", w);
    }
}
