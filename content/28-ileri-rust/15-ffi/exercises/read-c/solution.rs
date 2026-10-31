use std::ffi::{CStr, c_char};
use std::ptr;

/// # Safety
/// `pointer` must be null or a valid, NUL-terminated string.
unsafe fn read_c(pointer: *const c_char) -> Option<String> {
    if pointer.is_null() {
        return None;
    }
    // SAFETY: the caller promised a valid, NUL-terminated string.
    let text = unsafe { CStr::from_ptr(pointer) };
    text.to_str().ok().map(String::from)
}

fn main() {
    let text = unsafe { read_c(c"hello".as_ptr()) };
    println!("{text:?}");
    println!("{:?}", unsafe { read_c(ptr::null()) });
}
