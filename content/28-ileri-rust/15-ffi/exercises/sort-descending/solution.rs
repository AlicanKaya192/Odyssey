use std::ffi::{c_int, c_void};

unsafe extern "C" {
    fn qsort(
        base: *mut c_void,
        count: usize,
        size: usize,
        compare: extern "C" fn(*const c_void, *const c_void) -> c_int,
    );
}

extern "C" fn compare(a: *const c_void, b: *const c_void) -> c_int {
    // SAFETY: qsort gives pointers into the i32 slice we passed.
    let (a, b) = unsafe { (*(a as *const i32), *(b as *const i32)) };
    b.cmp(&a) as c_int
}

fn sort_descending(values: &mut [i32]) {
    // SAFETY: the pointer, count and size all describe the same slice.
    unsafe {
        qsort(values.as_mut_ptr().cast(), values.len(), size_of::<i32>(), compare);
    }
}

fn main() {
    let mut values = [3, -1, 2];
    sort_descending(&mut values);
    println!("{values:?}");
}
