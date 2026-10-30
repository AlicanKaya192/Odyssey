use std::sync::mpsc;
use std::thread;

// fn lengths ...

fn main() {
    println!("{:?}", lengths(vec![String::from("go"), String::from("rust")]));
}
