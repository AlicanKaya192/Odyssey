use std::alloc::{Layout, alloc, dealloc, handle_alloc_error};
use std::ops::{Deref, DerefMut};
use std::ptr;

pub struct MyBox<T> {
    pointer: *mut T,
}

// impl<T> MyBox<T> { pub fn new(value: T) -> Self ... }
// impl<T> Deref for MyBox<T> ...
// impl<T> DerefMut for MyBox<T> ...
// impl<T> Drop for MyBox<T> ...

fn main() {
    let mut boxed = MyBox::new(String::from("hi"));
    boxed.push('!');
    println!("{}", *boxed);
}
