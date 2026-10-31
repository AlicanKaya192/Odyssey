use my_macros::text_of;

fn main() {
    println!("{}", text_of!(hello));
    println!("{}", text_of!(a + 1));
    println!("{}", text_of!(Vec<u8>));
}
