fn add_through(a: &i32, b: &i32) -> i32 {
    let pa = a as *const i32;
    let pb = b as *const i32;
    // burada unsafe ile iki isaretciyi oku ve topla
    0
}

fn main() {
    println!("{}", add_through(&2, &3));
}
