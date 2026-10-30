use std::ptr;

fn replace_quietly(slot: &mut String, new: String) -> String {
    // SAFETY: the old value is returned and the slot is overwritten at once.
    unsafe {
        let old = ptr::read(slot);
        ptr::write(slot, new);
        old
    }
}

fn main() {
    let mut name = String::from("old");
    let previous = replace_quietly(&mut name, String::from("new"));
    println!("{previous} {name}");
}
