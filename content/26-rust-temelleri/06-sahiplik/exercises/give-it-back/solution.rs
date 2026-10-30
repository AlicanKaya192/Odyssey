fn add_title(name: String) -> String {
    let mut titled = name;
    titled.push_str(" the Great");
    titled
}

fn main() {
    let name = String::from("Ada");
    let name = add_title(name);
    println!("{name}");
}
