use std::cell::UnsafeCell;
use std::sync::atomic::{AtomicU8, Ordering};

const EMPTY: u8 = 0;
const WRITING: u8 = 1;
const READY: u8 = 2;

struct OnceValue<T> {
    state: AtomicU8,
    value: UnsafeCell<Option<T>>,
}

// SAFETY: the state orders the single write, and readers see only &T afterwards.
unsafe impl<T: Send + Sync> Sync for OnceValue<T> {}

impl<T> OnceValue<T> {
    fn new() -> Self {
        OnceValue { state: AtomicU8::new(EMPTY), value: UnsafeCell::new(None) }
    }

    fn set(&self, value: T) -> bool {
        if self.state.compare_exchange(EMPTY, WRITING, Ordering::Acquire, Ordering::Relaxed).is_err() {
            return false;
        }
        // SAFETY: only the branch moving EMPTY to WRITING reaches here.
        unsafe { *self.value.get() = Some(value) };
        self.state.store(READY, Ordering::Release);
        true
    }

    fn get(&self) -> Option<&T> {
        if self.state.load(Ordering::Acquire) != READY {
            return None;
        }
        // SAFETY: READY means the write is finished and never happens again.
        unsafe { (*self.value.get()).as_ref() }
    }
}

fn main() {
    let once = OnceValue::new();
    println!("{} {}", once.set(1), once.set(2));
    println!("{:?}", once.get());
}
