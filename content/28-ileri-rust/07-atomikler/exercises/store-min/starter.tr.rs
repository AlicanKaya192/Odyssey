use std::sync::atomic::{AtomicU32, Ordering};

// fn store_min(slot: &AtomicU32, value: u32) ...

fn main() {
    let slot = AtomicU32::new(5);
    store_min(&slot, 3);
    println!("{}", slot.load(Ordering::SeqCst));
}
