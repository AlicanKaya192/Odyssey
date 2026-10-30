fn is_prime(n: u32) -> bool {
    if n < 2 {
        return false;
    }
    let mut d = 2;
    while d * d <= n {
        if n % d == 0 {
            return false;
        }
        d += 1;
    }
    true
}

fn next_prime(n: u32) -> u32 {
    let mut candidate = n + 1;
    loop {
        if is_prime(candidate) {
            break candidate;
        }
        candidate += 1;
    }
}

fn main() {
    println!("{}", next_prime(14));
}
