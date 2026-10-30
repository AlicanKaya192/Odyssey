fn reverse_raw(list: &mut [i32]) {
    let len = list.len();
    let p = list.as_mut_ptr();
    for i in 0..len / 2 {
        // SAFETY: i and len - 1 - i are in bounds and are never the same.
        unsafe {
            let left = p.add(i);
            let right = p.add(len - 1 - i);
            let saved = *left;
            *left = *right;
            *right = saved;
        }
    }
}

fn main() {
    let mut list = [1, 2, 3];
    reverse_raw(&mut list);
    println!("{list:?}");
}
