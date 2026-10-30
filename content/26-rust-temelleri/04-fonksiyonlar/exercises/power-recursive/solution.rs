fn power(base: u64, exp: u32) -> u64 {
    if exp == 0 {
        return 1;
    }
    base * power(base, exp - 1)
}

fn main() {
    println!("{}", power(2, 10));
}
