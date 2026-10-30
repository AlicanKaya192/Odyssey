use std::fmt;

struct Duration {
    seconds: u32,
}

// impl fmt::Display ...

fn main() {
    println!("{}", Duration { seconds: 125 });
}
