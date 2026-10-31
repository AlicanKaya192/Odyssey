use my_macros::TypeName;

#[derive(TypeName)]
pub struct Point {
    x: i32,
}

#[derive(TypeName)]
enum Color {
    Red,
}

fn main() {
    println!("{}", Point::type_name());
    println!("{}", Color::type_name());
    let point = Point { x: 1 };
    let _ = (point.x, Color::Red);
}
