use std::mem::MaybeUninit;

struct TwoSlots {
    slots: [MaybeUninit<String>; 2],
    len: usize,
}

impl TwoSlots {
    fn new() -> Self {
        TwoSlots { slots: [const { MaybeUninit::uninit() }; 2], len: 0 }
    }

    // fn push(&mut self, text: String) -> bool ...
    // fn get(&self, i: usize) -> Option<&str> ...
}

// impl Drop for TwoSlots ...

fn main() {
    let mut t = TwoSlots::new();
    println!("{}", t.push(String::from("a")));
    println!("{:?}", t.get(0));
}
