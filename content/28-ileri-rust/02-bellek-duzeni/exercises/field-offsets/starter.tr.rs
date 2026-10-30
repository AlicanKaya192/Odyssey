use std::mem::offset_of;

#[repr(C)]
struct Point {
    a: u8,
    b: u16,
    c: u32,
}

// fn offsets() -> (usize, usize, usize) ...

fn main() {
    println!("{:?}", offsets());
}
