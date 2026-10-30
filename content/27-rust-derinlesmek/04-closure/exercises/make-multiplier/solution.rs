fn multiplier(n: i32) -> impl Fn(i32) -> i32 {
    move |x| x * n
}

fn main() {
    let triple = multiplier(3);
    println!("{}", triple(4));
}
