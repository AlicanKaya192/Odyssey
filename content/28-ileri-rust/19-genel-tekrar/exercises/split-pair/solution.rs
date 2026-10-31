use std::slice;

fn split_pair<T>(values: &mut [T], middle: usize) -> (&mut [T], &mut [T]) {
    assert!(middle <= values.len());
    let length = values.len();
    let start = values.as_mut_ptr();
    // SAFETY: the two parts do not overlap and stay inside the slice.
    unsafe {
        (
            slice::from_raw_parts_mut(start, middle),
            slice::from_raw_parts_mut(start.add(middle), length - middle),
        )
    }
}

fn main() {
    let mut values = [1, 2, 3, 4];
    let (left, right) = split_pair(&mut values, 1);
    left[0] = 10;
    right[0] = 20;
    println!("{values:?}");
}
