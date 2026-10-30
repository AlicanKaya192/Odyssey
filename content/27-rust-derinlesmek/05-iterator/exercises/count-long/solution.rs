fn long_words(text: &str, min: usize) -> usize {
    text.split_whitespace().filter(|w| w.len() >= min).count()
}

fn main() {
    println!("{}", long_words("a bcd ef", 2));
}
