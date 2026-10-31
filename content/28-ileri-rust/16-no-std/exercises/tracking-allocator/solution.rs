use std::alloc::{GlobalAlloc, Layout, System};
use std::sync::atomic::{AtomicUsize, Ordering};

struct Tracking;

static BYTES: AtomicUsize = AtomicUsize::new(0);

// SAFETY: every call is passed on to the system allocator unchanged.
unsafe impl GlobalAlloc for Tracking {
    unsafe fn alloc(&self, layout: Layout) -> *mut u8 {
        BYTES.fetch_add(layout.size(), Ordering::Relaxed);
        unsafe { System.alloc(layout) }
    }

    unsafe fn dealloc(&self, pointer: *mut u8, layout: Layout) {
        BYTES.fetch_sub(layout.size(), Ordering::Relaxed);
        unsafe { System.dealloc(pointer, layout) }
    }
}

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
