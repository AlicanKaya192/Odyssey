use std::sync::mpsc;
use std::thread;

fn run_workers(jobs: Vec<i32>) -> Vec<i32> {
    let (tx, rx) = mpsc::channel();
    for job in jobs {
        let tx = tx.clone();
        thread::spawn(move || {
            tx.send(job * 2).unwrap();
        });
    }
    drop(tx);
    let mut out: Vec<i32> = rx.iter().collect();
    out.sort();
    out
}

fn main() {
    println!("{:?}", run_workers(vec![3, 1, 2]));
}
