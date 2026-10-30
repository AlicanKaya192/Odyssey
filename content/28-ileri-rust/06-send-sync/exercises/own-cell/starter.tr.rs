use std::cell::UnsafeCell;

struct MyCell<T> {
    value: UnsafeCell<T>,
}

// impl<T: Copy> MyCell<T> { fn new ... fn get ... fn set ... fn update ... }

fn main() {
    let c = MyCell::new(1);
    c.update(|n| n + 1);
    println!("{}", c.get());
}
