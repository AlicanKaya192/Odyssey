use std::io;

fn main() {
    let mut line = String::new();
    io::stdin().read_line(&mut line).expect("could not read");
    let total: i32 = line.trim().parse().expect("not a number");
    println!("{:02}:{:02}", total / 60, total % 60);
}
