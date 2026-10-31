use tiny::{Buffer, report};

fn main() {
    let mut storage = [0u8; 8];
    let mut buffer = Buffer::new(&mut storage);
    println!("{:?}", report(&mut buffer, "a", 5));
    println!("{}", str::from_utf8(buffer.as_bytes()).unwrap());

    let mut storage = [0u8; 2];
    let mut buffer = Buffer::new(&mut storage);
    println!("{:?}", report(&mut buffer, "long", 5));
    println!("{}", buffer.as_bytes().len() <= 2);
}
