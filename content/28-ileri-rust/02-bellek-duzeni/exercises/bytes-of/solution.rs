fn bytes_of(n: u32) -> [u8; 4] {
    let p = &raw const n as *const u8;
    let mut out = [0; 4];
    for i in 0..4 {
        // SAFETY: a u32 has four bytes, and any byte value is a valid u8.
        out[i] = unsafe { *p.add(i) };
    }
    out
}

fn main() {
    println!("{:?}", bytes_of(1));
}
