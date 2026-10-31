use std::marker::PhantomPinned;
use std::pin::Pin;
use std::ptr;

struct SelfRef {
    value: String,
    pointer: *const String,
    _pin: PhantomPinned,
}

// impl SelfRef {
//     fn new(text: &str) -> Pin<Box<Self>> ...
//     fn read(self: Pin<&Self>) -> &str ...
// }

fn main() {
    let a = SelfRef::new("hello");
    let moved = a;
    println!("{}", moved.as_ref().read());
}
