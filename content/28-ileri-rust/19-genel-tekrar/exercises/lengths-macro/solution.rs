use std::ffi::{CString, c_char};

unsafe extern "C" {
    fn strlen(text: *const c_char) -> usize;
}

fn c_len(text: &str) -> usize {
    let text = CString::new(text).unwrap();
    // SAFETY: text is a valid, NUL-terminated string for the whole call.
    unsafe { strlen(text.as_ptr()) }
}

macro_rules! lengths {
    ( $( $text:expr ),* $(,)? ) => {
        vec![ $( c_len($text) ),* ]
    };
}

fn main() {
    println!("{:?}", lengths!("a", "bcd", "ef"));
    println!("{:?}", lengths!("x",));
    let none: Vec<usize> = lengths!();
    println!("{none:?}");
}
