struct Evens {
    next_value: u32,
}

impl Iterator for Evens {
    type Item = u32;

    fn next(&mut self) -> Option<u32> {
        let out = self.next_value;
        self.next_value += 2;
        Some(out)
    }
}

fn main() {
    let v: Vec<u32> = Evens { next_value: 0 }.take(3).collect();
    println!("{:?}", v);
}
