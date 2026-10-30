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

    fn push(&self, value: T) {
        let node = Box::into_raw(Box::new(Node { value, next: ptr::null_mut() }));
        let mut head = self.head.load(Ordering::Relaxed);
        loop {
            // SAFETY: the node is not shared yet.
            unsafe { (*node).next = head };
            let result = self.head.compare_exchange_weak(
                head,
                node,
                Ordering::Release,
                Ordering::Relaxed,
            );
            match result {
                Ok(_) => return,
                Err(actual) => head = actual,
            }
        }
    }

    fn take_all(&self) -> Vec<T> {
        let mut current = self.head.swap(ptr::null_mut(), Ordering::Acquire);
        let mut out = Vec::new();
        while !current.is_null() {
            // SAFETY: swap gave the whole chain to this branch alone.
            let node = unsafe { Box::from_raw(current) };
            current = node.next;
            out.push(node.value);
        }
        out
    }
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
