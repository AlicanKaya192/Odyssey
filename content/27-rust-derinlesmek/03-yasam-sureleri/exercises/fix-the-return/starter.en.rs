fn make_greeting(name: &str) -> &str {
    let text = format!("Hello, {name}!");
    &text
}

fn main() {
    println!("{}", make_greeting("Ada"));
}
