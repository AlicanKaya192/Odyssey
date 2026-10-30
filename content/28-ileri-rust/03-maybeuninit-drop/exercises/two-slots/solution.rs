use std::mem::MaybeUninit;

struct TwoSlots {
    slots: [MaybeUninit<String>; 2],
    len: usize,
}

impl TwoSlots {
    fn new() -> Self {
        TwoSlots { slots: [const { MaybeUninit::uninit() }; 2], len: 0 }
    }

    fn push(&mut self, text: String) -> bool {
        if self.len == self.slots.len() {
            return false;
        }
        self.slots[self.len].write(text);
        self.len += 1;
        true
    }

    fn get(&self, i: usize) -> Option<&str> {
        if i >= self.len {
            return None;
        }
        // SAFETY: every slot below len was written.
        Some(unsafe { self.slots[i].assume_init_ref() })
    }
}

impl Drop for TwoSlots {
    fn drop(&mut self) {
        for slot in &mut self.slots[..self.len] {
            // SAFETY: every slot below len was written and is dropped once.
            unsafe { slot.assume_init_drop() };
        }
    }
}

fn main() {
    let mut t = TwoSlots::new();
    println!("{}", t.push(String::from("a")));
    println!("{:?}", t.get(0));
}
