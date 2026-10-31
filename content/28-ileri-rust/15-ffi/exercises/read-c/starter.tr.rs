use std::ffi::{CStr, c_char};
use std::ptr;

// unsafe fn read_c(pointer: *const c_char) -> Option<String> ...

fn main() {
    let text = unsafe { read_c(c"hello".as_ptr()) };
    println!("{text:?}");
    println!("{:?}", unsafe { read_c(ptr::null()) });
}
