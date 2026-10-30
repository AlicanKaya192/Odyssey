use std::sync::atomic::{AtomicU32, Ordering};
use std::thread;

fn count_even(list: &[u32]) -> u32 {
    let count = AtomicU32::new(0);
    thread::scope(|s| {
        for part in list.chunks(2) {
            let count = &count;
            s.spawn(move || {
                for n in part {
                    if n % 2 == 0 {
                        count.fetch_add(1, Ordering::SeqCst);
                    }
                }
            });
        }
    });
    count.load(Ordering::SeqCst)
}

fn main() {
    println!("{}", count_even(&[1, 2, 3, 4, 6]));
}
