use my_macros::Show;

#[derive(Show)]
struct Point {
    x: i32,
    y: i32,
}

#[derive(Show)]
struct User {
    name: std::string::String,
    age: u8,
    tags: Vec<u8>,
}

fn main() {
    println!("{}", Point { x: 1, y: 2 }.show());
    let user = User { name: String::from("ada"), age: 36, tags: vec![1, 2] };
    println!("{}", user.show());
}
