use std::marker::PhantomData;
use std::ops::{Deref, DerefMut};
use std::ptr::NonNull;

struct MyBox<T> {
    ptr: NonNull<T>,
    _owns: PhantomData<T>,
}

// impl<T> MyBox<T> { fn new(value: T) -> Self ... }
// impl<T> Deref for MyBox<T> ...
// impl<T> DerefMut for MyBox<T> ...
// impl<T> Drop for MyBox<T> ...

fn main() {
    let mut b = MyBox::new(1);
    *b += 1;
    println!("{}", *b);
}
