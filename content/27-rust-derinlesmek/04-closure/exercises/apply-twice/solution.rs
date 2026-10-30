fn apply_twice<F: Fn(i32) -> i32>(f: F, value: i32) -> i32 {
    f(f(value))
}

fn main() {
    println!("{}", apply_twice(|x| x + 3, 1));
}
