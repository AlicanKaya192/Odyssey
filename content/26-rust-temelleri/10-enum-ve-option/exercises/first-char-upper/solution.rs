fn initial(name: Option<&str>) -> char {
    if let Some(text) = name {
        if let Some(first) = text.chars().next() {
            return first.to_ascii_uppercase();
        }
    }
    '?'
}

fn main() {
    println!("{}", initial(Some("ada")));
    println!("{}", initial(None));
}
