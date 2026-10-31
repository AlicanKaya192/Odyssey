use std::sync::atomic::{AtomicU32, Ordering};
use std::thread;

// fn store_max(target: &AtomicU32, value: u32) ...

fn main() {
    let highest = AtomicU32::new(0);
    thread::scope(|s| {
        for start in 0..4u32 {
            let highest = &highest;
            s.spawn(move || {
                for value in 0..1000 {
                    store_max(highest, start * 1000 + value);
                }
            });
        }
    });
    println!("{}", highest.load(Ordering::Relaxed));
}
