use std::sync::atomic::{AtomicBool, AtomicU32, Ordering};
use std::thread;

struct Slot {
    data: AtomicU32,
    ready: AtomicBool,
}

fn publish(slot: &Slot, value: u32) {
    slot.data.store(value, Ordering::Relaxed);
    slot.ready.store(true, Ordering::Release);
}

fn wait_for(slot: &Slot) -> u32 {
    while !slot.ready.load(Ordering::Acquire) {
        std::hint::spin_loop();
    }
    slot.data.load(Ordering::Relaxed)
}

fn main() {
    let slot = Slot { data: AtomicU32::new(0), ready: AtomicBool::new(false) };
    thread::scope(|s| {
        s.spawn(|| publish(&slot, 9));
        println!("{}", wait_for(&slot));
    });
}
