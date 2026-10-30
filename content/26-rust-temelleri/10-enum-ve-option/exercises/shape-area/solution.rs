enum Shape {
    Circle { radius: f64 },
    Rect { width: f64, height: f64 },
    Square(f64),
}

impl Shape {
    fn area(&self) -> f64 {
        match self {
            Shape::Circle { radius } => std::f64::consts::PI * radius * radius,
            Shape::Rect { width, height } => width * height,
            Shape::Square(side) => side * side,
        }
    }
}

fn main() {
    println!("{}", Shape::Square(3.0).area());
}
