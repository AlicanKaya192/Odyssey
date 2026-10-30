fn main() {
    let text = String::from("hello");

    #[cfg(feature = "shout")]
    let text = text.to_uppercase();

    println!("{text}");
}
