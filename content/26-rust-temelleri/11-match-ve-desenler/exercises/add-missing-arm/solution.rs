enum Shape {
    Square(f64),
    Triangle { base: f64, height: f64 },
}

fn area(shape: &Shape) -> f64 {
    match shape {
        Shape::Square(side) => side * side,
        Shape::Triangle { base, height } => base * height / 2.0,
    }
}

fn main() {
    println!("{}", area(&Shape::Square(2.0)));
}
