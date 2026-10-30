use std::sync::atomic::{AtomicBool, AtomicU32, Ordering};
use std::thread;

struct Slot {
    data: AtomicU32,
    ready: AtomicBool,
}

// fn publish(slot: &Slot, value: u32) ...
// fn wait_for(slot: &Slot) -> u32 ...

fn main() {
    let slot = Slot { data: AtomicU32::new(0), ready: AtomicBool::new(false) };
    thread::scope(|s| {
        s.spawn(|| publish(&slot, 9));
        println!("{}", wait_for(&slot));
    });
}
