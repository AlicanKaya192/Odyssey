fn first_word(text: &str) -> &str {
    for (position, letter) in text.char_indices() {
        if letter == ' ' {
            return &text[..position];
        }
    }
    text
}

fn main() {
    println!("{}", first_word("hello world"));
}
