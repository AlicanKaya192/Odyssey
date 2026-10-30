fn add_suffix(text: &mut String) {
    text.push_str(".rs");
}

fn main() {
    let mut file = String::from("main");
    add_suffix(&mut file);
    println!("{file}");
}
