fn largest<T: PartialOrd>(list: &[T]) -> Option<&T> {
    let mut top = list.first()?;
    for item in list {
        if item > top {
            top = item;
        }
    }
    Some(top)
}

fn main() {
    println!("{:?}", largest(&[3, 9, 2]));
}
