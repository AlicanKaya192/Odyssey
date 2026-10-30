use std::sync::atomic::{AtomicBool, Ordering};

struct Once {
    done: AtomicBool,
}

impl Once {
    fn new() -> Self {
        Once { done: AtomicBool::new(false) }
    }

    // fn try_claim(&self) -> bool ...
}

fn main() {
    let once = Once::new();
    println!("{} {}", once.try_claim(), once.try_claim());
}
