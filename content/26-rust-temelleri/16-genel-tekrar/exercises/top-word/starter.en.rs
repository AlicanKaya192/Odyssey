use std::collections::BTreeMap;

// fn word_counts ...
// fn most_common ...

fn main() {
    let counts = word_counts("a b A");
    println!("{:?}", most_common(&counts));
}
