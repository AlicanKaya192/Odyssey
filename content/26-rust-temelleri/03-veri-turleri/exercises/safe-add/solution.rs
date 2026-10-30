fn main() {
    let step = "abcdefghij".len() as u8;
    let mut level: u8 = 250;
    level = level.saturating_add(step);
    println!("level: {level}");
}
