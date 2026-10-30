use std::sync::Mutex;
use std::thread;

// fn parallel_sum(list: &[i64], parts: usize) -> i64 ...

fn main() {
    println!("{}", parallel_sum(&[1, 2, 3, 4, 5], 2));
}
