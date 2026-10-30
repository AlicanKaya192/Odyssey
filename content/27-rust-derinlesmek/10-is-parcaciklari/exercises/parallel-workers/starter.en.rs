use std::sync::mpsc;
use std::thread;

// fn run_workers ...

fn main() {
    println!("{:?}", run_workers(vec![3, 1, 2]));
}
