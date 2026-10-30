/// Returns the item at `i`.
///
/// # Safety
///
/// `i` must be smaller than `list.len()`.
unsafe fn item_unchecked(list: &[i32], i: usize) -> i32 {
    // SAFETY: the caller guarantees i is in bounds.
    unsafe { *list.get_unchecked(i) }
}

fn last_item(list: &[i32]) -> Option<i32> {
    if list.is_empty() {
        return None;
    }
    // SAFETY: len - 1 is in bounds because the list is not empty.
    Some(unsafe { item_unchecked(list, list.len() - 1) })
}

fn main() {
    println!("{:?}", last_item(&[1, 2]));
}
