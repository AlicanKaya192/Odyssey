fn count_a(text: String) -> usize {
    text.matches('a').count()
}

fn main() {
    let word = String::from("banana");
    let n = count_a(word);
    println!("{word}: {n}");
}
