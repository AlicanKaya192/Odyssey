use std::ptr;

// unsafe fn read_or(p: *const i32, default: i32) -> i32 ...

fn main() {
    let value = 3;
    // SAFETY: both pointers are valid or null.
    unsafe {
        println!("{}", read_or(&value, 0));
        println!("{}", read_or(ptr::null(), 9));
    }
}
