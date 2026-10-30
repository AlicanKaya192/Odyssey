fn run(steps: &[Box<dyn Fn(i32) -> i32>], start: i32) -> i32 {
    let mut value = start;
    for step in steps {
        value = step(value);
    }
    value
}

fn add(n: i32) -> Box<dyn Fn(i32) -> i32> {
    Box::new(move |x| x + n)
}

fn main() {
    println!("{}", run(&[add(2), Box::new(|x| x * 3)], 1));
}
