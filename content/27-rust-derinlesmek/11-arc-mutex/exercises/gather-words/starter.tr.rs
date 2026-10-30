use std::sync::{Arc, Mutex};
use std::thread;

// fn gather ...

fn main() {
    println!("{:?}", gather(vec![String::from("b"), String::from("a")]));
}
