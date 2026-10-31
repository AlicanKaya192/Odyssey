use std::alloc::{GlobalAlloc, Layout, System};
use std::sync::atomic::{AtomicUsize, Ordering};

struct Tracking;

static BYTES: AtomicUsize = AtomicUsize::new(0);

// unsafe impl GlobalAlloc for Tracking ...

#[global_allocator]
static ALLOCATOR: Tracking = Tracking;

fn main() {
    let before = BYTES.load(Ordering::Relaxed);
    let values = std::hint::black_box(vec![0u8; 1024]);
    let during = BYTES.load(Ordering::Relaxed);
    drop(values);
    let after = BYTES.load(Ordering::Relaxed);
    println!("{}", during - before);
    println!("{}", after - before);
}
