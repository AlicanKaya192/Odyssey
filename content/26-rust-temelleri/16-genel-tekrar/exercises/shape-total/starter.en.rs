#[derive(Debug)]
enum Shape {
    Circle(f64),
    Rect { w: f64, h: f64 },
}

// fn area ...
// fn total_area ...

fn main() {
    let shapes = [Shape::Circle(1.0), Shape::Rect { w: 2.0, h: 3.0 }];
    println!("{}", total_area(&shapes));
}
