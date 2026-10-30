fn safe_divide(a: i32, b: i32) -> Option<i32> {
    if b == 0 {
        None
    } else {
        Some(a / b)
    }
}

fn main() {
    println!("{:?}", safe_divide(10, 2));
    println!("{:?}", safe_divide(1, 0));
}
