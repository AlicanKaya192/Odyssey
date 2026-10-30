fn scale(values: &mut [i32; 4], factor: i32) {
    for n in values.iter_mut() {
        *n *= factor;
    }
}

fn main() {
    let mut data = [1, 2, 3, 4];
    scale(&mut data, 10);
    println!("{:?}", data);
}
