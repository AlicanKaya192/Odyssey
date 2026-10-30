use std::marker::PhantomData;
use std::ops::{Deref, DerefMut};
use std::ptr::NonNull;

struct MyBox<T> {
    ptr: NonNull<T>,
    _owns: PhantomData<T>,
}

impl<T> MyBox<T> {
    fn new(value: T) -> Self {
        let raw = Box::into_raw(Box::new(value));
        // SAFETY: Box::into_raw never gives null.
        let ptr = unsafe { NonNull::new_unchecked(raw) };
        MyBox { ptr, _owns: PhantomData }
    }
}

impl<T> Deref for MyBox<T> {
    type Target = T;

    fn deref(&self) -> &T {
        // SAFETY: ptr is valid until Drop.
        unsafe { self.ptr.as_ref() }
    }
}

impl<T> DerefMut for MyBox<T> {
    fn deref_mut(&mut self) -> &mut T {
        // SAFETY: ptr is valid until Drop, and &mut self is unique.
        unsafe { self.ptr.as_mut() }
    }
}

impl<T> Drop for MyBox<T> {
    fn drop(&mut self) {
        // SAFETY: ptr came from Box::into_raw and is taken back once.
        unsafe { drop(Box::from_raw(self.ptr.as_ptr())) };
    }
}

fn main() {
    let mut b = MyBox::new(1);
    *b += 1;
    println!("{}", *b);
}
