struct Countdown {
    current: u32,
}

// impl Iterator ...

fn main() {
    println!("{:?}", Countdown { current: 3 }.collect::<Vec<u32>>());
}
