use std::sync::atomic::{AtomicU32, Ordering};

fn store_min(slot: &AtomicU32, value: u32) {
    let mut current = slot.load(Ordering::SeqCst);
    while value < current {
        match slot.compare_exchange(current, value, Ordering::SeqCst, Ordering::SeqCst) {
            Ok(_) => return,
            Err(actual) => current = actual,
        }
    }
}

fn main() {
    let slot = AtomicU32::new(5);
    store_min(&slot, 3);
    println!("{}", slot.load(Ordering::SeqCst));
}
