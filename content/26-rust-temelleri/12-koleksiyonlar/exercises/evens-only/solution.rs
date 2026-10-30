fn evens(values: &[i32]) -> Vec<i32> {
    let mut out = Vec::new();
    for v in values {
        if v % 2 == 0 {
            out.push(*v);
        }
    }
    out
}

fn main() {
    println!("{:?}", evens(&[1, 2, 3, 4]));
}
