use std::sync::{mpsc, Arc, Mutex};
use std::thread;

fn pool(jobs: Vec<i32>, workers: usize) -> Vec<i32> {
    let (job_tx, job_rx) = mpsc::channel::<i32>();
    let (out_tx, out_rx) = mpsc::channel();
    let job_rx = Arc::new(Mutex::new(job_rx));
    for _ in 0..workers {
        let job_rx = Arc::clone(&job_rx);
        let out_tx = out_tx.clone();
        thread::spawn(move || loop {
            let job = job_rx.lock().unwrap().recv();
            match job {
                Ok(n) => out_tx.send(n + 1).unwrap(),
                Err(_) => break,
            }
        });
    }
    drop(out_tx);
    for j in jobs {
        job_tx.send(j).unwrap();
    }
    drop(job_tx);
    let mut got: Vec<i32> = out_rx.iter().collect();
    got.sort();
    got
}

fn main() {
    println!("{:?}", pool(vec![1, 2, 3], 2));
}
