use std::ptr;

// fn replace_quietly(slot: &mut String, new: String) -> String ...

fn main() {
    let mut name = String::from("old");
    let previous = replace_quietly(&mut name, String::from("new"));
    println!("{previous} {name}");
}
