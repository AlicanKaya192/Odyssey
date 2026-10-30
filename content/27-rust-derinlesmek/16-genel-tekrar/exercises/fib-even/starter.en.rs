struct Fib {
    a: u64,
    b: u64,
}

fn fib() -> Fib {
    Fib { a: 1, b: 2 }
}

// impl Iterator for Fib ...

// fn even_sum(limit: u64) -> u64 ...

fn main() {
    println!("{}", even_sum(100));
}
