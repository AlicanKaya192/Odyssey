use std::sync::{Arc, Mutex};
use std::thread;

fn count_up(branches: usize, each: u32) -> u32 {
    let counter = Arc::new(Mutex::new(0));
    let mut handles = Vec::new();
    for _ in 0..branches {
        let counter = Arc::clone(&counter);
        handles.push(thread::spawn(move || {
            for _ in 0..each {
                *counter.lock().unwrap() += 1;
            }
        }));
    }
    for h in handles {
        h.join().unwrap();
    }
    let total = *counter.lock().unwrap();
    total
}

fn main() {
    println!("{}", count_up(4, 100));
}
