#[derive(Debug)]
enum Shape {
    Circle(f64),
    Rect { w: f64, h: f64 },
}

fn area(shape: &Shape) -> f64 {
    match shape {
        Shape::Circle(r) => 3.0 * r * r,
        Shape::Rect { w, h } => w * h,
    }
}

fn total_area(shapes: &[Shape]) -> f64 {
    let mut total = 0.0;
    for shape in shapes {
        total += area(shape);
    }
    total
}

fn main() {
    let shapes = [Shape::Circle(1.0), Shape::Rect { w: 2.0, h: 3.0 }];
    println!("{}", total_area(&shapes));
}
