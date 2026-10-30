trait Shape {
    fn area(&self) -> u32;
    fn name(&self) -> String;
}

struct Square(u32);
struct Rect(u32, u32);

impl Shape for Square {
    fn area(&self) -> u32 {
        self.0 * self.0
    }
    fn name(&self) -> String {
        String::from("square")
    }
}

impl Shape for Rect {
    fn area(&self) -> u32 {
        self.0 * self.1
    }
    fn name(&self) -> String {
        String::from("rect")
    }
}

fn total_area(shapes: &[Box<dyn Shape>]) -> u32 {
    shapes.iter().map(|s| s.area()).sum()
}

fn biggest_name(shapes: &[Box<dyn Shape>]) -> Option<String> {
    shapes.iter().max_by_key(|s| s.area()).map(|s| s.name())
}

fn main() {
    let shapes: Vec<Box<dyn Shape>> = vec![Box::new(Square(2)), Box::new(Rect(2, 3))];
    println!("{}", total_area(&shapes));
}
