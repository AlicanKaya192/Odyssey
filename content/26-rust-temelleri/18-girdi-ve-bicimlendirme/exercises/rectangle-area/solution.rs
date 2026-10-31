use std::io;

fn main() {
    let mut line = String::new();
    io::stdin().read_line(&mut line).expect("could not read");
    let width: f64 = line.trim().parse().expect("not a number");

    line.clear();
    io::stdin().read_line(&mut line).expect("could not read");
    let height: f64 = line.trim().parse().expect("not a number");

    println!("area: {:.2}", width * height);
}
