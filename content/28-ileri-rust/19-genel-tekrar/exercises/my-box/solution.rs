use std::alloc::{Layout, alloc, dealloc, handle_alloc_error};
use std::ops::{Deref, DerefMut};
use std::ptr;

pub struct MyBox<T> {
    pointer: *mut T,
}

impl<T> MyBox<T> {
    pub fn new(value: T) -> Self {
        let layout = Layout::new::<T>();
        assert!(layout.size() > 0, "zero-sized types are not supported");
        // SAFETY: the layout has a non-zero size.
        let pointer = unsafe { alloc(layout) }.cast::<T>();
        if pointer.is_null() {
            handle_alloc_error(layout);
        }
        // SAFETY: the pointer is valid and aligned for a T.
        unsafe { ptr::write(pointer, value) };
        MyBox { pointer }
    }
}

impl<T> Deref for MyBox<T> {
    type Target = T;

    fn deref(&self) -> &T {
        // SAFETY: new wrote a value, and drop has not run.
        unsafe { &*self.pointer }
    }
}

impl<T> DerefMut for MyBox<T> {
    fn deref_mut(&mut self) -> &mut T {
        // SAFETY: as above, and &mut self is unique.
        unsafe { &mut *self.pointer }
    }
}

impl<T> Drop for MyBox<T> {
    fn drop(&mut self) {
        // SAFETY: the value is alive, and the pointer came from alloc with this layout.
        unsafe {
            ptr::drop_in_place(self.pointer);
            dealloc(self.pointer.cast(), Layout::new::<T>());
        }
    }
}

fn main() {
    let mut boxed = MyBox::new(String::from("hi"));
    boxed.push('!');
    println!("{}", *boxed);
}
