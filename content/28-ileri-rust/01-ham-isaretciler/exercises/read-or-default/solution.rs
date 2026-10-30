use std::ptr;

/// Reads `p`, or returns `default` if it is null.
///
/// # Safety
///
/// If `p` is not null, it must point to a live `i32`.
unsafe fn read_or(p: *const i32, default: i32) -> i32 {
    // SAFETY: the caller guarantees a non-null p is valid.
    match unsafe { p.as_ref() } {
        Some(value) => *value,
        None => default,
    }
}

fn main() {
    let value = 3;
    // SAFETY: both pointers are valid or null.
    unsafe {
        println!("{}", read_or(&value, 0));
        println!("{}", read_or(ptr::null(), 9));
    }
}
