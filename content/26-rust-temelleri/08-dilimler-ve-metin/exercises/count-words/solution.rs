fn word_count(text: &str) -> usize {
    text.split_whitespace().count()
}

fn main() {
    println!("{}", word_count("rust is  fun"));
}
