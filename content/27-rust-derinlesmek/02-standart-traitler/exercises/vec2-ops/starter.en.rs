use std::ops::{Add, Mul};

// struct Vec2 ...

fn main() {
    let a = Vec2 { x: 1.0, y: 2.0 };
    println!("{:?}", (a + a) * 0.5);
}
