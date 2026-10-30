fn make_greeter(name: String) -> impl Fn() -> String {
    || format!("Hello, {name}")
}

fn main() {
    let greet = make_greeter(String::from("Ada"));
    println!("{}", greet());
}
