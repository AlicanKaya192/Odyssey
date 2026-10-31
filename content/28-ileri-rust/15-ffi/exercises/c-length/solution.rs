use std::ffi::{CString, c_char};

unsafe extern "C" {
    fn strlen(text: *const c_char) -> usize;
}

fn c_length(text: &str) -> Option<usize> {
    let text = CString::new(text).ok()?;
    // SAFETY: text is a valid, NUL-terminated string for the whole call.
    Some(unsafe { strlen(text.as_ptr()) })
}

fn main() {
    println!("{:?}", c_length("hello"));
    println!("{:?}", c_length("a\0b"));
}
