use std::mem::offset_of;

#[repr(C)]
struct Point {
    a: u8,
    b: u16,
    c: u32,
}

fn offsets() -> (usize, usize, usize) {
    (offset_of!(Point, a), offset_of!(Point, b), offset_of!(Point, c))
}

fn main() {
    println!("{:?}", offsets());
}
