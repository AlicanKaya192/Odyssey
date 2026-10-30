fn main() {
    for row in 1..=3 {
        for col in 1..=3 {
            print!("{:>3}", row * col);
        }
        println!();
    }
}
