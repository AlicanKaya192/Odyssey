use std::marker::PhantomPinned;
use std::pin::Pin;
use std::ptr;

struct SelfRef {
    value: String,
    pointer: *const String,
    _pin: PhantomPinned,
}

impl SelfRef {
    fn new(text: &str) -> Pin<Box<Self>> {
        let mut boxed = Box::pin(SelfRef {
            value: text.to_string(),
            pointer: ptr::null(),
            _pin: PhantomPinned,
        });
        let pointer: *const String = &boxed.value;
        // SAFETY: writing a field does not move the struct.
        unsafe { boxed.as_mut().get_unchecked_mut().pointer = pointer };
        boxed
    }

    fn read(self: Pin<&Self>) -> &str {
        // SAFETY: the struct is pinned, so the pointer still shows its field.
        unsafe { &*self.pointer }
    }
}

fn main() {
    let a = SelfRef::new("hello");
    let moved = a;
    println!("{}", moved.as_ref().read());
}
