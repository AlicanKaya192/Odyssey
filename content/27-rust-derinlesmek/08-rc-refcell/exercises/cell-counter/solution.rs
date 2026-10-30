use std::cell::Cell;

struct Stats {
    calls: Cell<u32>,
}

impl Stats {
    fn new() -> Stats {
        Stats { calls: Cell::new(0) }
    }

    fn hit(&self) {
        self.calls.set(self.calls.get() + 1);
    }
}

fn main() {
    let s = Stats::new();
    s.hit();
    s.hit();
    println!("{}", s.calls.get());
}
