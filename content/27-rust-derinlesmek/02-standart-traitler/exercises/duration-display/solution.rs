use std::fmt;

struct Duration {
    seconds: u32,
}

impl fmt::Display for Duration {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{}m {:02}s", self.seconds / 60, self.seconds % 60)
    }
}

fn main() {
    println!("{}", Duration { seconds: 125 });
}
