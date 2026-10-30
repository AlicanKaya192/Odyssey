fn divide(a: i32, b: i32) -> (i32, i32) {
    (a / b, a % b)
}

fn main() {
    let (quotient, rest) = divide(17, 5);
    println!("17 / 5 = {quotient} rest {rest}");
}
