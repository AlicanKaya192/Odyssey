use std::sync::atomic::{AtomicU32, Ordering};
use std::thread;

// fn count_even(list: &[u32]) -> u32 ...

fn main() {
    println!("{}", count_even(&[1, 2, 4]));
}
