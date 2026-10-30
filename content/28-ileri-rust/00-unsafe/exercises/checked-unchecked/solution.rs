fn get_or_zero(list: &[i32], i: usize) -> i32 {
    if i >= list.len() {
        return 0;
    }
    // SAFETY: i < len was checked just above.
    unsafe { *list.get_unchecked(i) }
}

fn main() {
    println!("{}", get_or_zero(&[5, 6], 1));
}
