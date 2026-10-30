use std::sync::{Arc, Mutex};
use std::thread;

fn count_up(n: u32) -> u32 {
    let total = Arc::new(Mutex::new(0));
    let copy = Arc::clone(&total);
    let handle = thread::spawn(move || {
        for _ in 0..n {
            *copy.lock().unwrap() += 1;
        }
    });
    handle.join().unwrap();
    let result = *total.lock().unwrap();
    result
}

fn main() {
    println!("{}", count_up(5));
}
