fn dot(a: &[i32], b: &[i32]) -> i32 {
    a.iter().zip(b.iter()).map(|(x, y)| x * y).sum()
}

fn main() {
    println!("{}", dot(&[1, 2], &[3, 4]));
}
