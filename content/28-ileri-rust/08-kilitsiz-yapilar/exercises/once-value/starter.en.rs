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

    // fn set(&self, value: T) -> bool ...
    // fn get(&self) -> Option<&T> ...
}

fn main() {
    let once = OnceValue::new();
    println!("{} {}", once.set(1), once.set(2));
    println!("{:?}", once.get());
}
