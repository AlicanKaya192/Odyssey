// fn largest_by<T, F>(list: &[T], key: F) -> Option<&T> ...

fn main() {
    let words = ["a", "ccc", "bb"];
    println!("{:?}", largest_by(&words, |w| w.len()));
}
