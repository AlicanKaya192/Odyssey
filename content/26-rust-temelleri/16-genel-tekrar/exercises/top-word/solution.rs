use std::collections::BTreeMap;

fn word_counts(text: &str) -> BTreeMap<String, u32> {
    let mut counts = BTreeMap::new();
    for word in text.split_whitespace() {
        *counts.entry(word.to_lowercase()).or_insert(0) += 1;
    }
    counts
}

fn most_common(counts: &BTreeMap<String, u32>) -> Option<&str> {
    let mut best: Option<(&str, u32)> = None;
    for (word, count) in counts {
        match best {
            Some((_, top)) if top >= *count => {}
            _ => best = Some((word, *count)),
        }
    }
    best.map(|(word, _)| word)
}

fn main() {
    let counts = word_counts("a b A");
    println!("{:?}", most_common(&counts));
}
