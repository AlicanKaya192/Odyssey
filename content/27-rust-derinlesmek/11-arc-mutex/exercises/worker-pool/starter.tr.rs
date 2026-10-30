use std::sync::{mpsc, Arc, Mutex};
use std::thread;

// fn pool ...

fn main() {
    println!("{:?}", pool(vec![1, 2, 3], 2));
}
