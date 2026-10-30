use std::collections::HashMap;

fn top_word(text: &str) -> Option<String> {
    let mut counts: HashMap<&str, u32> = HashMap::new();
    for word in text.split_whitespace() {
        *counts.entry(word).or_insert(0) += 1;
    }
    counts
        .into_iter()
        .max_by_key(|(word, count)| (*count, std::cmp::Reverse(*word)))
        .map(|(word, _)| word.to_string())
}

fn main() {
    println!("{:?}", top_word("a b b c"));
}
