fn append_through_raw(text: String, tail: &str) -> String {
    let p = Box::into_raw(Box::new(text));
    // SAFETY: p came from Box::into_raw and is taken back exactly once.
    unsafe {
        (*p).push_str(tail);
        *Box::from_raw(p)
    }
}

fn main() {
    println!("{}", append_through_raw(String::from("a"), "b"));
}
