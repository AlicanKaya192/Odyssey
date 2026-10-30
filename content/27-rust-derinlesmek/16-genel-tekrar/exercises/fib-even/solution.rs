struct Fib {
    a: u64,
    b: u64,
}

fn fib() -> Fib {
    Fib { a: 1, b: 2 }
}

impl Iterator for Fib {
    type Item = u64;

    fn next(&mut self) -> Option<u64> {
        let value = self.a;
        self.a = self.b;
        self.b += value;
        Some(value)
    }
}

fn even_sum(limit: u64) -> u64 {
    fib().take_while(|n| *n <= limit).filter(|n| n % 2 == 0).sum()
}

fn main() {
    println!("{}", even_sum(100));
}
