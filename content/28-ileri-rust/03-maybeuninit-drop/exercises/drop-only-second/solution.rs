use std::mem::ManuallyDrop;
use std::sync::atomic::{AtomicU32, Ordering};

static DROPS: AtomicU32 = AtomicU32::new(0);

struct Counted;

impl Drop for Counted {
    fn drop(&mut self) {
        DROPS.fetch_add(1, Ordering::SeqCst);
    }
}

fn drop_only_second() -> u32 {
    let _first = ManuallyDrop::new(Counted);
    let mut second = ManuallyDrop::new(Counted);
    // SAFETY: second is not used after this line.
    unsafe { ManuallyDrop::drop(&mut second) };
    DROPS.load(Ordering::SeqCst)
}

fn main() {
    println!("{}", drop_only_second());
}
