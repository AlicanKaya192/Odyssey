#[repr(u8)]
#[derive(Debug, PartialEq, Clone, Copy)]
enum Level {
    Low = 1,
    Mid = 2,
    High = 10,
}

fn code(level: Level) -> u8 {
    level as u8
}

fn from_code(n: u8) -> Option<Level> {
    match n {
        1 => Some(Level::Low),
        2 => Some(Level::Mid),
        10 => Some(Level::High),
        _ => None,
    }
}

fn main() {
    println!("{}", code(Level::High));
}
