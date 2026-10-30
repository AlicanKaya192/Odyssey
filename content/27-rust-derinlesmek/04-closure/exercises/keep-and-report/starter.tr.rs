// fn keep ...
// fn each_total ...

fn main() {
    let limit = 2;
    println!("{:?}", keep(&[1, 2, 3], |n| n > limit));
    let mut seen = Vec::new();
    each_total(&[1, 2, 3], |t| seen.push(t));
    println!("{:?}", seen);
}
