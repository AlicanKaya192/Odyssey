use std::thread;

fn two_sums(left: &[i32], right: &[i32]) -> (i32, i32) {
    thread::scope(|s| {
        let a = s.spawn(|| left.iter().sum::<i32>());
        let b = s.spawn(|| right.iter().sum::<i32>());
        (a.join().unwrap(), b.join().unwrap())
    })
}

fn main() {
    println!("{:?}", two_sums(&[1, 2], &[3, 4]));
}
