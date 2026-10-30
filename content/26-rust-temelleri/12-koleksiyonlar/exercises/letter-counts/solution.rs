use std::collections::BTreeMap;

fn letter_counts(text: &str) -> BTreeMap<char, u32> {
    let mut counts = BTreeMap::new();
    for letter in text.chars() {
        if letter != ' ' {
            *counts.entry(letter).or_insert(0) += 1;
        }
    }
    counts
}

fn main() {
    println!("{:?}", letter_counts("aba c"));
}
