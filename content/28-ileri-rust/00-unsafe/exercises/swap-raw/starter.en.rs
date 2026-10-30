fn swap_values(a: &mut i32, b: &mut i32) {
    let pa = a as *mut i32;
    let pb = b as *mut i32;
    // swap with raw pointers
}

fn main() {
    let (mut x, mut y) = (1, 2);
    swap_values(&mut x, &mut y);
    println!("{x} {y}");
}
