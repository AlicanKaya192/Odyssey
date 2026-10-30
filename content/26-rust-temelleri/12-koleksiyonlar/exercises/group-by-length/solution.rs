use std::collections::BTreeMap;

fn group_by_length(words: &[&str]) -> BTreeMap<usize, Vec<String>> {
    let mut groups: BTreeMap<usize, Vec<String>> = BTreeMap::new();
    for word in words {
        groups.entry(word.len()).or_default().push(word.to_string());
    }
    groups
}

fn main() {
    println!("{:?}", group_by_length(&["go", "rust", "c", "java", "ml"]));
}
