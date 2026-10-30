fn first_even(values: &[i32]) -> Option<i32> {
    for v in values {
        if v % 2 == 0 {
            return Some(*v);
        }
    }
    None
}

fn main() {
    println!("{:?}", first_even(&[1, 3, 4, 6]));
}
