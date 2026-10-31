use std::io;

fn main() {
    let mut line = String::new();
    io::stdin().read_line(&mut line).expect("could not read");
    let n: i32 = line.trim().parse().expect("not a number");
    println!("{}", n * 2);
}
