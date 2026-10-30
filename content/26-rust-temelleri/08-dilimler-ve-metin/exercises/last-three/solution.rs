fn last_three(values: &[i32]) -> &[i32] {
    if values.len() <= 3 {
        return values;
    }
    &values[values.len() - 3..]
}

fn main() {
    println!("{:?}", last_three(&[1, 2, 3, 4, 5]));
}
