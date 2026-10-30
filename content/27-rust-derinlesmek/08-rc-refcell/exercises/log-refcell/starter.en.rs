use std::cell::RefCell;

struct Log {
    lines: RefCell<Vec<String>>,
}

// impl Log ...

fn main() {
    let log = Log::new();
    log.write("a");
    println!("{}", log.count());
}
