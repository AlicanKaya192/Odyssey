fn main() {
    let pair = (17, 42);
    let (a, b) = pair;
    println!("max: {}", a.max(b));
    println!("min: {}", a.min(b));
}
