fn main() {
    let n = 472;
    let hundreds = n / 100;
    let tens = n / 10 % 10;
    let ones = n % 10;
    println!("{hundreds} {tens} {ones}");
    println!("sum: {}", hundreds + tens + ones);
}
