use std::sync::atomic::{AtomicU64, Ordering};
use std::thread;

static NEXT: AtomicU64 = AtomicU64::new(1);

// fn next_id() -> u64 ...

fn main() {
    println!("{} {}", next_id() > 0, next_id() > 1);
    let handle = thread::spawn(next_id);
    println!("{}", handle.join().unwrap() > 2);
}
