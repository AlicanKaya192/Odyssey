fn reversed(text: &str) -> String {
    text.chars().rev().collect()
}

fn main() {
    println!("{}", reversed("rust"));
}
