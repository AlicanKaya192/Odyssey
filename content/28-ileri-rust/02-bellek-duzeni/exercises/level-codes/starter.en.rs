// #[repr(u8)] enum Level { Low = 1, Mid = 2, High = 10 }
// fn code(level: Level) -> u8 ...
// fn from_code(n: u8) -> Option<Level> ...

fn main() {
    println!("{}", code(Level::High));
}
