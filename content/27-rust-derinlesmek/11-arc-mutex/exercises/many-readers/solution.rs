use std::sync::{Arc, RwLock};
use std::thread;

fn read_all(value: i32, readers: usize) -> i32 {
    let shared = Arc::new(RwLock::new(value));
    let mut handles = Vec::new();
    for _ in 0..readers {
        let shared = Arc::clone(&shared);
        handles.push(thread::spawn(move || *shared.read().unwrap()));
    }
    let mut total = 0;
    for h in handles {
        total += h.join().unwrap();
    }
    total
}

fn main() {
    println!("{}", read_all(5, 3));
}
