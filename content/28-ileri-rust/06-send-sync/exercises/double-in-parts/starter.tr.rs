use std::thread;

struct SendPtr(*mut i32);

// SAFETY: each branch writes only to its own part of the list.
unsafe impl Send for SendPtr {}

impl SendPtr {
    fn get(&self) -> *mut i32 {
        self.0
    }
}

// fn double_in_parts(list: &mut [i32]) ...

fn main() {
    let mut list = [1, 2, 3];
    double_in_parts(&mut list);
    println!("{list:?}");
}
