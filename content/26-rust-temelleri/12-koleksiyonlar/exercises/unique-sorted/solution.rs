fn unique_sorted(values: &[i32]) -> Vec<i32> {
    let mut out = values.to_vec();
    out.sort();
    out.dedup();
    out
}

fn main() {
    println!("{:?}", unique_sorted(&[3, 1, 3, 2, 1]));
}
