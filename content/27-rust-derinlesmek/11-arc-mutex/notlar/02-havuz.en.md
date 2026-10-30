## A worker pool

Jobs on a channel, a fixed number of workers. Since `rx` is single, it is shared with `Arc<Mutex<...>>`:

```rust
use std::sync::{mpsc, Arc, Mutex};
use std::thread;

fn main() {
    let (job_tx, job_rx) = mpsc::channel::<i32>();
    let (out_tx, out_rx) = mpsc::channel();
    let job_rx = Arc::new(Mutex::new(job_rx));
    for _ in 0..3 {
        let job_rx = Arc::clone(&job_rx);
        let out_tx = out_tx.clone();
        thread::spawn(move || loop {
            let job = job_rx.lock().unwrap().recv();
            match job {
                Ok(n) => out_tx.send(n * n).unwrap(),
                Err(_) => break,
            }
        });
    }
    drop(out_tx);
    for n in 1..=5 {
        job_tx.send(n).unwrap();
    }
    drop(job_tx);
    let mut got: Vec<i32> = out_rx.iter().collect();
    got.sort();
    println!("{:?}", got);
}
```

```text
[1, 4, 9, 16, 25]
```

The flow:

<figure class="fig"><div class="flow"><span class="node">main: send</span><span class="arrow">→</span><span class="node">Arc&lt;Mutex&lt;rx&gt;&gt;</span><span class="arrow">→</span><span class="node ok">worker</span><span class="arrow">→</span><span class="node">result channel</span></div><figcaption>Workers take jobs in turn and write results to a separate channel.</figcaption></figure>

**Careful:** the line `let job = rx.lock().unwrap().recv();` releases the guard when that line ends. If `while let Ok(job) = rx.lock().unwrap().recv()` were written, the lock would be held through the loop body and jobs would not run at once. This is a common error in real programs.

## Small rules

- While holding a lock, `println!` is slow too, and files or networks are slower.
- Do not call a closure while holding a lock: you do not know what is inside.
- `.lock().unwrap()` may stay on one line: the guard drops at the line's end.
- A `Vec<Mutex<T>>` may scale better than one large lock.
