fn swap<A, B>(pair: (A, B)) -> (B, A) {
    let (a, b) = pair;
    (b, a)
}

fn main() {
    println!("{:?}", swap((1, "one")));
}
