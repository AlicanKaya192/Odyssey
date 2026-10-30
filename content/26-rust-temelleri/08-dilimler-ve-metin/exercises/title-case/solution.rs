fn title_case(text: &str) -> String {
    let mut out = String::new();
    for word in text.split_whitespace() {
        if !out.is_empty() {
            out.push(' ');
        }
        let mut letters = word.chars();
        if let Some(first) = letters.next() {
            out.push_str(&first.to_uppercase().to_string());
            out.push_str(&letters.as_str().to_lowercase());
        }
    }
    out
}

fn main() {
    println!("{}", title_case("rUST  is fun"));
}
