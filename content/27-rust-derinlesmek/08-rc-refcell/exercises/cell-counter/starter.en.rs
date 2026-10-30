use std::cell::Cell;

struct Stats {
    calls: Cell<u32>,
}

// impl Stats ...

fn main() {
    let s = Stats::new();
    s.hit();
    s.hit();
    println!("{}", s.calls.get());
}
