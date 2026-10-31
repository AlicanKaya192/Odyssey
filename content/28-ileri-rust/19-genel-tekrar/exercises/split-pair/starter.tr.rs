use std::slice;

// fn split_pair<T>(values: &mut [T], middle: usize) -> (&mut [T], &mut [T]) ...

fn main() {
    let mut values = [1, 2, 3, 4];
    let (left, right) = split_pair(&mut values, 1);
    left[0] = 10;
    right[0] = 20;
    println!("{values:?}");
}
