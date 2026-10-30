enum Shape {
    Square(f64),
    Triangle { base: f64, height: f64 },
}

fn area(shape: &Shape) -> f64 {
    match shape {
        Shape::Square(side) => side * side,
    }
}

fn main() {
    println!("{}", area(&Shape::Square(2.0)));
}
