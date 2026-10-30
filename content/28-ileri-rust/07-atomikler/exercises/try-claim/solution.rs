use std::sync::atomic::{AtomicBool, Ordering};

struct Once {
    done: AtomicBool,
}

impl Once {
    fn new() -> Self {
        Once { done: AtomicBool::new(false) }
    }

    fn try_claim(&self) -> bool {
        self.done
            .compare_exchange(false, true, Ordering::AcqRel, Ordering::Acquire)
            .is_ok()
    }
}

fn main() {
    let once = Once::new();
    println!("{} {}", once.try_claim(), once.try_claim());
}
