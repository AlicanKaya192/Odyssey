struct Countdown {
    current: u32,
}

impl Iterator for Countdown {
    type Item = u32;

    fn next(&mut self) -> Option<u32> {
        if self.current == 0 {
            return None;
        }
        let out = self.current;
        self.current -= 1;
        Some(out)
    }
}

fn main() {
    println!("{:?}", Countdown { current: 3 }.collect::<Vec<u32>>());
}
