use std::alloc::{self, Layout};
use std::ptr::{self, NonNull};

struct MyVec<T> {
    ptr: NonNull<T>,
    cap: usize,
    len: usize,
}

impl<T> MyVec<T> {
    fn new() -> Self {
        assert!(size_of::<T>() != 0, "zero-sized types are not handled");
        MyVec { ptr: NonNull::dangling(), cap: 0, len: 0 }
    }

    fn grow(&mut self) {
        let new_cap = if self.cap == 0 { 4 } else { self.cap * 2 };
        let new_layout = Layout::array::<T>(new_cap).unwrap();

        let new_ptr = if self.cap == 0 {
            // SAFETY: T is not zero-sized, so the layout size is not zero.
            unsafe { alloc::alloc(new_layout) }
        } else {
            let old_layout = Layout::array::<T>(self.cap).unwrap();
            let old_ptr = self.ptr.as_ptr().cast::<u8>();
            // SAFETY: old_ptr came from alloc with old_layout.
            unsafe { alloc::realloc(old_ptr, old_layout, new_layout.size()) }
        };

        self.ptr = match NonNull::new(new_ptr.cast::<T>()) {
            Some(p) => p,
            None => alloc::handle_alloc_error(new_layout),
        };
        self.cap = new_cap;
    }
}

impl<T> MyVec<T> {
    fn push(&mut self, value: T) {
        if self.len == self.cap {
            self.grow();
        }
        // SAFETY: len < cap, so the place is inside the allocation and empty.
        unsafe { ptr::write(self.ptr.as_ptr().add(self.len), value) };
        self.len += 1;
    }

    fn pop(&mut self) -> Option<T> {
        if self.len == 0 {
            return None;
        }
        self.len -= 1;
        // SAFETY: the place was filled, and len no longer covers it.
        Some(unsafe { ptr::read(self.ptr.as_ptr().add(self.len)) })
    }
}

impl<T> Drop for MyVec<T> {
    fn drop(&mut self) {
        while self.pop().is_some() {}
        if self.cap != 0 {
            let layout = Layout::array::<T>(self.cap).unwrap();
            // SAFETY: ptr came from alloc or realloc with this layout.
            unsafe { alloc::dealloc(self.ptr.as_ptr().cast::<u8>(), layout) };
        }
    }
}

impl<T> MyVec<T> {
    fn insert(&mut self, index: usize, value: T) {
        assert!(index <= self.len, "index out of bounds");
        if self.len == self.cap {
            self.grow();
        }
        // SAFETY: index <= len < cap, and copy allows overlap.
        unsafe {
            let p = self.ptr.as_ptr().add(index);
            ptr::copy(p, p.add(1), self.len - index);
            ptr::write(p, value);
        }
        self.len += 1;
    }

    fn remove(&mut self, index: usize) -> T {
        assert!(index < self.len, "index out of bounds");
        // SAFETY: index < len, so the value exists and is taken out once.
        unsafe {
            let p = self.ptr.as_ptr().add(index);
            let value = ptr::read(p);
            ptr::copy(p.add(1), p, self.len - index - 1);
            self.len -= 1;
            value
        }
    }
}

fn main() {
    let mut v = MyVec::new();
    v.insert(0, 2);
    v.insert(0, 1);
    println!("{}", v.remove(0));
}
