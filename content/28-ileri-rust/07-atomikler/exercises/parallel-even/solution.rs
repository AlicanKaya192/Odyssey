use std::sync::atomic::{AtomicU32, Ordering};
use std::thread;

fn count_even(list: &[u32]) -> u32 {
    let count = AtomicU32::new(0);
    thread::scope(|s| {
        for chunk in list.chunks(2) {
            let count = &count;
            s.spawn(move || {
                for n in chunk {
                    if n % 2 == 0 {
                        count.fetch_add(1, Ordering::Relaxed);
                    }
                }
            });
        }
    });
    count.load(Ordering::Relaxed)
}

fn main() {
    println!("{}", count_even(&[1, 2, 4]));
}
