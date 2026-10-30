mod stats;

fn main() {
    println!("{:?}", stats::mean(&[1.0, 2.0, 6.0]));
}
