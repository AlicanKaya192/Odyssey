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

fn squares(n: u32) -> Vec<u32> {
    let mut out = Vec::with_capacity(n as usize);
    for i in 0..n {
        out.push(i * i);
    }
    out
}

fn main() {
    println!("{}", count_of(|| {
        black_box(squares(1000));
    }));
    println!("{:?}", squares(4));
    println!("{:?}", squares(0));
}
