struct Counter {
    value: u32,
}

impl Counter {
    fn new() -> Self {
        Self { value: 0 }
    }

    fn increment(&mut self) {
        self.value += 1;
    }

    fn reset(&mut self) {
        self.value = 0;
    }

    fn value(&self) -> u32 {
        self.value
    }
}

fn main() {
    let mut c = Counter::new();
    c.increment();
    c.increment();
    println!("{}", c.value());
}
