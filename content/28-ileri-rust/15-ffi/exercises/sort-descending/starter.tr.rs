use std::ffi::{c_int, c_void};

unsafe extern "C" {
    fn qsort(
        base: *mut c_void,
        count: usize,
        size: usize,
        compare: extern "C" fn(*const c_void, *const c_void) -> c_int,
    );
}

// extern "C" fn compare ...
// fn sort_descending(values: &mut [i32]) ...

fn main() {
    let mut values = [3, -1, 2];
    sort_descending(&mut values);
    println!("{values:?}");
}
