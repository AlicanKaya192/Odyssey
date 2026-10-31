use std::alloc::{GlobalAlloc, Layout, System};
use std::hint::black_box;
use std::sync::atomic::{AtomicUsize, Ordering};

struct Counting;

static COUNT: AtomicUsize = AtomicUsize::new(0);

// SAFETY: every call is passed on to the system allocator unchanged.
unsafe impl GlobalAlloc for Counting {
    unsafe fn alloc(&self, layout: Layout) -> *mut u8 {
        COUNT.fetch_add(1, Ordering::Relaxed);
        unsafe { System.alloc(layout) }
    }

    unsafe fn dealloc(&self, pointer: *mut u8, layout: Layout) {
        unsafe { System.dealloc(pointer, layout) }
    }

    unsafe fn realloc(&self, pointer: *mut u8, layout: Layout, size: usize) -> *mut u8 {
        COUNT.fetch_add(1, Ordering::Relaxed);
        unsafe { System.realloc(pointer, layout, size) }
    }
}

#[global_allocator]
static ALLOCATOR: Counting = Counting;

fn count_of(work: impl FnOnce()) -> usize {
    let before = COUNT.load(Ordering::Relaxed);
    work();
    COUNT.load(Ordering::Relaxed) - before
}

fn upper_total(words: &[&str]) -> usize {
    let mut buffer = String::with_capacity(32);
    let mut total = 0;
    for word in words {
        buffer.clear();
        buffer.push_str(word);
        buffer.make_ascii_uppercase();
        total += black_box(&buffer).len();
    }
    total
}

fn main() {
    let words = ["alpha", "beta", "gamma", "delta", "epsilon"];
    let mut total = 0;
    let count = count_of(|| {
        total = upper_total(&words);
    });
    println!("{total}");
    println!("under two: {}", count < 2);
}
