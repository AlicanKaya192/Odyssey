struct Evens {
    next_value: u32,
}

// impl Iterator ...

fn main() {
    let v: Vec<u32> = Evens { next_value: 0 }.take(3).collect();
    println!("{:?}", v);
}
