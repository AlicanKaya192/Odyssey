fn search(pattern: &str, text: &str) -> Vec<String> {
    let mut found = Vec::new();
    for (index, line) in text.lines().enumerate() {
        if line.contains(pattern) {
            found.push(format!("{}: {}", index + 1, line));
        }
    }
    found
}

fn main() {
    println!("{:?}", search("b", "a\nb"));
}
