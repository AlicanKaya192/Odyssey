use std::ffi::{CString, c_char};

unsafe extern "C" {
    fn strlen(text: *const c_char) -> usize;
}

// fn c_length(text: &str) -> Option<usize> ...

fn main() {
    println!("{:?}", c_length("hello"));
    println!("{:?}", c_length("a\0b"));
}
