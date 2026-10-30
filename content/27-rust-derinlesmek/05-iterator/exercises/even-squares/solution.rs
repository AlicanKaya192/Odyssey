fn even_squares(values: &[i32]) -> Vec<i32> {
    values.iter().filter(|x| **x % 2 == 0).map(|x| x * x).collect()
}

fn main() {
    println!("{:?}", even_squares(&[1, 2, 3, 4]));
}
