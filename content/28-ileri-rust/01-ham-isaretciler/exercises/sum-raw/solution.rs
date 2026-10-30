fn sum_raw(list: &[i32]) -> i32 {
    let p = list.as_ptr();
    let mut total = 0;
    for i in 0..list.len() {
        // SAFETY: i < len, so p.add(i) is inside the slice.
        total += unsafe { *p.add(i) };
    }
    total
}

fn main() {
    println!("{}", sum_raw(&[1, 2, 3]));
}
