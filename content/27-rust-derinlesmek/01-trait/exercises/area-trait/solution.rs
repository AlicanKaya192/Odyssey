trait Area {
    fn area(&self) -> f64;

    fn is_large(&self) -> bool {
        self.area() > 100.0
    }
}

struct Square(f64);
struct Rect(f64, f64);

impl Area for Square {
    fn area(&self) -> f64 {
        self.0 * self.0
    }
}

impl Area for Rect {
    fn area(&self) -> f64 {
        self.0 * self.1
    }
}

fn main() {
    println!("{}", Square(2.0).area());
    println!("{}", Rect(20.0, 6.0).is_large());
}
