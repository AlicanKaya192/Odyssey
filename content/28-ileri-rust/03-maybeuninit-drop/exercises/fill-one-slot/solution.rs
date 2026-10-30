use std::mem::MaybeUninit;

fn fill_slot(text: &str) -> String {
    let mut slot = MaybeUninit::<String>::uninit();
    slot.write(text.to_uppercase());
    // SAFETY: the value was written on the line above.
    unsafe { slot.assume_init() }
}

fn main() {
    println!("{}", fill_slot("hi"));
}
