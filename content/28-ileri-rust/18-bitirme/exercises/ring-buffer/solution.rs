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

impl<T, const N: usize> Producer<'_, T, N> {
    pub fn push(&mut self, value: T) -> Result<(), T> {
        let tail = self.ring.tail.load(Ordering::Relaxed);
        let head = self.ring.head.load(Ordering::Acquire);
        if tail - head == N {
            return Err(value);
        }
        let slot = self.ring.slots[tail % N].get();
        // SAFETY: this slot is empty, and only this producer writes.
        unsafe { (*slot).write(value) };
        self.ring.tail.store(tail + 1, Ordering::Release);
        Ok(())
    }
}

impl<T, const N: usize> Consumer<'_, T, N> {
    pub fn pop(&mut self) -> Option<T> {
        let head = self.ring.head.load(Ordering::Relaxed);
        let tail = self.ring.tail.load(Ordering::Acquire);
        if head == tail {
            return None;
        }
        let slot = self.ring.slots[head % N].get();
        // SAFETY: Acquire saw this slot written, and only this consumer reads.
        let value = unsafe { (*slot).assume_init_read() };
        self.ring.head.store(head + 1, Ordering::Release);
        Some(value)
    }
}

impl<T, const N: usize> Drop for Ring<T, N> {
    fn drop(&mut self) {
        let (head, tail) = (*self.head.get_mut(), *self.tail.get_mut());
        for index in head..tail {
            // SAFETY: slots from head to tail hold values nobody has read.
            unsafe { self.slots[index % N].get_mut().assume_init_drop() };
        }
    }
}

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
