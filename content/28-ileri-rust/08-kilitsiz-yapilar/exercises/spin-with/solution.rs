use std::cell::UnsafeCell;
use std::sync::atomic::{AtomicBool, Ordering};
use std::thread;

struct SpinLock<T> {
    locked: AtomicBool,
    value: UnsafeCell<T>,
}

// SAFETY: the flag gives one access at a time.
unsafe impl<T: Send> Sync for SpinLock<T> {}

impl<T> SpinLock<T> {
    fn new(value: T) -> Self {
        SpinLock { locked: AtomicBool::new(false), value: UnsafeCell::new(value) }
    }

    fn with<R>(&self, work: impl FnOnce(&mut T) -> R) -> R {
        while self
            .locked
            .compare_exchange_weak(false, true, Ordering::Acquire, Ordering::Relaxed)
            .is_err()
        {
            std::hint::spin_loop();
        }
        // SAFETY: the flag was taken, so this branch has the only access.
        let result = work(unsafe { &mut *self.value.get() });
        self.locked.store(false, Ordering::Release);
        result
    }
}

fn main() {
    let lock = SpinLock::new(1);
    println!("{}", lock.with(|n| { *n += 1; *n }));
    thread::scope(|s| {
        s.spawn(|| lock.with(|n| *n += 1));
    });
}
