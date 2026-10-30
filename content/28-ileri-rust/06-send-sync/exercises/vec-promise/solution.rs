use std::ptr::NonNull;
use std::thread;

struct MyVec<T> {
    ptr: NonNull<T>,
    len: usize,
}

impl<T> MyVec<T> {
    fn from_one(value: T) -> Self {
        let raw = Box::into_raw(Box::new(value));
        // SAFETY: Box::into_raw never gives null.
        MyVec { ptr: unsafe { NonNull::new_unchecked(raw) }, len: 1 }
    }

    fn first(&self) -> &T {
        // SAFETY: ptr is valid until Drop.
        unsafe { self.ptr.as_ref() }
    }
}

impl<T> Drop for MyVec<T> {
    fn drop(&mut self) {
        // SAFETY: ptr came from Box::into_raw and is taken back once.
        unsafe { drop(Box::from_raw(self.ptr.as_ptr())) };
    }
}

// SAFETY: MyVec owns its items, like Vec.
unsafe impl<T: Send> Send for MyVec<T> {}
// SAFETY: &MyVec gives only &T.
unsafe impl<T: Sync> Sync for MyVec<T> {}

fn main() {
    let list = MyVec::from_one(5);
    let handle = thread::spawn(move || println!("{}", list.first()));
    handle.join().unwrap();
}
