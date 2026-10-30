fn collatz_steps(n: u64) -> u32 {
    let mut value = n;
    let mut steps = 0;
    while value != 1 {
        value = if value % 2 == 0 { value / 2 } else { 3 * value + 1 };
        steps += 1;
    }
    steps
}

fn main() {
    println!("{}", collatz_steps(6));
}
