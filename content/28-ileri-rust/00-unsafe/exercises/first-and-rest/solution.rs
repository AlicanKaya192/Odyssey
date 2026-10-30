use std::slice;

fn first_and_rest(list: &mut [i32]) -> Option<(&mut i32, &mut [i32])> {
    if list.is_empty() {
        return None;
    }
    let len = list.len();
    let p = list.as_mut_ptr();
    // SAFETY: the list has at least one item, and the two parts do not overlap.
    unsafe { Some((&mut *p, slice::from_raw_parts_mut(p.add(1), len - 1))) }
}

fn main() {
    let mut list = [1, 2, 3];
    if let Some((first, rest)) = first_and_rest(&mut list) {
        *first = 10;
        rest[0] = 20;
    }
    println!("{list:?}");
}
