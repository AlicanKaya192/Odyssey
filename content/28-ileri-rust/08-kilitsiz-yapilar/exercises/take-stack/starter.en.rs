use std::ptr;
use std::sync::atomic::{AtomicPtr, Ordering};
use std::thread;

struct Node<T> {
    value: T,
    next: *mut Node<T>,
}

struct TakeStack<T> {
    head: AtomicPtr<Node<T>>,
}

// SAFETY: values move between branches, and the head is atomic.
unsafe impl<T: Send> Sync for TakeStack<T> {}

impl<T> TakeStack<T> {
    fn new() -> Self {
        TakeStack { head: AtomicPtr::new(ptr::null_mut()) }
    }

    // fn push(&self, value: T) ...
    // fn take_all(&self) -> Vec<T> ...
}

impl<T> Drop for TakeStack<T> {
    fn drop(&mut self) {
        self.take_all();
    }
}

fn main() {
    let stack = TakeStack::new();
    stack.push(1);
    stack.push(2);
    println!("{:?}", stack.take_all());
}
