fn matches(pattern: &str, line: &str, ignore_case: bool) -> bool {
    if ignore_case {
        line.to_lowercase().contains(&pattern.to_lowercase())
    } else {
        line.contains(pattern)
    }
}

fn main() {
    println!("{}", matches("RUST", "rust", true));
}
