use std::slice;

#[repr(transparent)]
struct Celsius(f64);

fn as_numbers(list: &[Celsius]) -> &[f64] {
    // SAFETY: Celsius has the layout of f64.
    unsafe { slice::from_raw_parts(list.as_ptr().cast::<f64>(), list.len()) }
}

fn main() {
    println!("{:?}", as_numbers(&[Celsius(1.5)]));
}
