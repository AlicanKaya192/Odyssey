fn make_greeting(name: &str) -> String {
    format!("Hello, {name}!")
}

fn main() {
    println!("{}", make_greeting("Ada"));
}
