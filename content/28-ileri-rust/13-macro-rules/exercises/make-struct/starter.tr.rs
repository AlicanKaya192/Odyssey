// macro_rules! make_struct ...

make_struct!(Point { x: i32, y: i32 });

fn main() {
    let point = Point { x: 3, y: 4 };
    println!("{} {}", point.x(), point.y());
}
