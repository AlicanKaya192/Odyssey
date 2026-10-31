use std::collections::HashSet;

// fn count_common(first: &[u32], second: &[u32]) -> usize ...

fn main() {
    let first: Vec<u32> = (0..200_000).collect();
    let second: Vec<u32> = (100_000..300_000).collect();
    println!("{}", count_common(&first, &second));
    println!("{}", count_common(&[1, 2, 2, 3], &[2, 3, 4]));
    println!("{}", count_common(&[], &[1]));
}
