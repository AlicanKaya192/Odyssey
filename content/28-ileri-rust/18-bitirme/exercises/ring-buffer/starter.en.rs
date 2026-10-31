use std::cell::UnsafeCell;
use std::mem::MaybeUninit;
use std::sync::atomic::{AtomicUsize, Ordering};
use std::thread;

pub struct Ring<T, const N: usize> {
    slots: [UnsafeCell<MaybeUninit<T>>; N],
    head: AtomicUsize,
    tail: AtomicUsize,
}

// SAFETY: head and tail hand each slot between one producer and one consumer.
unsafe impl<T: Send, const N: usize> Sync for Ring<T, N> {}

impl<T, const N: usize> Ring<T, N> {
    pub fn new() -> Self {
        Ring {
            slots: std::array::from_fn(|_| UnsafeCell::new(MaybeUninit::uninit())),
            head: AtomicUsize::new(0),
            tail: AtomicUsize::new(0),
        }
    }

    pub fn split(&mut self) -> (Producer<'_, T, N>, Consumer<'_, T, N>) {
        (Producer { ring: self }, Consumer { ring: self })
    }
}

pub struct Producer<'a, T, const N: usize> {
    ring: &'a Ring<T, N>,
}

pub struct Consumer<'a, T, const N: usize> {
    ring: &'a Ring<T, N>,
}

// impl<T, const N: usize> Producer<'_, T, N> { pub fn push(&mut self, value: T) -> Result<(), T> ... }
// impl<T, const N: usize> Consumer<'_, T, N> { pub fn pop(&mut self) -> Option<T> ... }
// impl<T, const N: usize> Drop for Ring<T, N> ...

fn main() {
    let mut ring = Ring::<u32, 16>::new();
    let (mut producer, mut consumer) = ring.split();
    let sum = thread::scope(|s| {
        s.spawn(move || {
            for value in 1..=100_000 {
                let mut value = value;
                while let Err(back) = producer.push(value) {
                    value = back;
                    thread::yield_now();
                }
            }
        });
        let mut sum = 0u64;
        let mut seen = 0;
        while seen < 100_000 {
            match consumer.pop() {
                Some(value) => {
                    sum += u64::from(value);
                    seen += 1;
                }
                None => thread::yield_now(),
            }
        }
        sum
    });
    println!("{sum}");
}
