fn largest_by<T, F>(list: &[T], key: F) -> Option<&T>
where
    F: Fn(&T) -> usize,
{
    let mut best = list.first()?;
    for item in list {
        if key(item) > key(best) {
            best = item;
        }
    }
    Some(best)
}

fn main() {
    let words = ["a", "ccc", "bb"];
    println!("{:?}", largest_by(&words, |w| w.len()));
}
