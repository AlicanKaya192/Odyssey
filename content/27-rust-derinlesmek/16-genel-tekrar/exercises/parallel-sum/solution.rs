use std::sync::Mutex;
use std::thread;

fn parallel_sum(list: &[i64], parts: usize) -> i64 {
    let total = Mutex::new(0);
    let size = list.len().div_ceil(parts).max(1);
    thread::scope(|s| {
        for part in list.chunks(size) {
            let total = &total;
            s.spawn(move || {
                let sum: i64 = part.iter().sum();
                *total.lock().unwrap() += sum;
            });
        }
    });
    total.into_inner().unwrap()
}

fn main() {
    println!("{}", parallel_sum(&[1, 2, 3, 4, 5], 2));
}
