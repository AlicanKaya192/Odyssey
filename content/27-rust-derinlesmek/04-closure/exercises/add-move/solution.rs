fn make_greeter(name: String) -> impl Fn() -> String {
    move || format!("Hello, {name}")
}

fn main() {
    let greet = make_greeter(String::from("Ada"));
    println!("{}", greet());
}
