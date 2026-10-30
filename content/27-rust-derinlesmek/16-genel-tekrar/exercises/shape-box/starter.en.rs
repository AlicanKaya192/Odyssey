trait Shape {
    fn area(&self) -> u32;
    fn name(&self) -> String;
}

struct Square(u32);
struct Rect(u32, u32);

// impl Shape for Square ...
// impl Shape for Rect ...

// fn total_area(shapes: &[Box<dyn Shape>]) -> u32 ...
// fn biggest_name(shapes: &[Box<dyn Shape>]) -> Option<String> ...

fn main() {
    let shapes: Vec<Box<dyn Shape>> = vec![Box::new(Square(2)), Box::new(Rect(2, 3))];
    println!("{}", total_area(&shapes));
}
