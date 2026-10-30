struct Rectangle {
    width: u32,
    height: u32,
}

// impl Rectangle { ... }

fn main() {
    let r = Rectangle { width: 3, height: 4 };
    println!("{} {}", r.area(), r.perimeter());
}
