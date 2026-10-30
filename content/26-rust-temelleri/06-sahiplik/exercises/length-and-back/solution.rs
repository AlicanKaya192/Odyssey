fn with_length(text: String) -> (String, usize) {
    let length = text.len();
    (text, length)
}

fn main() {
    let (text, n) = with_length(String::from("ownership"));
    println!("{text} {n}");
}
