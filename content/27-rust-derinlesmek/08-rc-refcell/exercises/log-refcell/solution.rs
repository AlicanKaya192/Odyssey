use std::cell::RefCell;

struct Log {
    lines: RefCell<Vec<String>>,
}

impl Log {
    fn new() -> Log {
        Log { lines: RefCell::new(Vec::new()) }
    }

    fn write(&self, line: &str) {
        self.lines.borrow_mut().push(line.to_string());
    }

    fn count(&self) -> usize {
        self.lines.borrow().len()
    }
}

fn main() {
    let log = Log::new();
    log.write("a");
    println!("{}", log.count());
}
