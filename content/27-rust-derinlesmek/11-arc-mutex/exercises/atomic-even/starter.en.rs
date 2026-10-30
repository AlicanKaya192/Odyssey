use std::sync::atomic::{AtomicU32, Ordering};
use std::thread;

// fn count_even ...

fn main() {
    println!("{}", count_even(&[1, 2, 3, 4, 6]));
}
