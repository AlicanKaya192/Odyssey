use std::thread;

struct SendPtr(*mut i32);

// SAFETY: each branch writes only to its own part of the list.
unsafe impl Send for SendPtr {}

impl SendPtr {
    fn get(&self) -> *mut i32 {
        self.0
    }
}

fn double_in_parts(list: &mut [i32]) {
    let len = list.len();
    let mid = len / 2;
    let left = SendPtr(list.as_mut_ptr());
    // SAFETY: mid <= len, so the pointer stays inside the slice.
    let right = SendPtr(unsafe { list.as_mut_ptr().add(mid) });
    thread::scope(|s| {
        s.spawn(move || {
            for i in 0..mid {
                // SAFETY: i < mid, and this part belongs only to this branch.
                unsafe { *left.get().add(i) *= 2 };
            }
        });
        s.spawn(move || {
            for i in 0..len - mid {
                // SAFETY: mid + i < len, and this part belongs only to this branch.
                unsafe { *right.get().add(i) *= 2 };
            }
        });
    });
}

fn main() {
    let mut list = [1, 2, 3];
    double_in_parts(&mut list);
    println!("{list:?}");
}
