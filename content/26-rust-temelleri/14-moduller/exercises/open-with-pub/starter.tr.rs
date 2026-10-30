mod shapes {
    fn area(w: u32, h: u32) -> u32 {
        helper(w) * h
    }

    fn helper(n: u32) -> u32 {
        n
    }
}

fn main() {
    println!("{}", shapes::area(3, 4));
}
