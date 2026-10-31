mod rt;

use rt::{executor, run};
use std::collections::BinaryHeap;
use std::future::Future;
use std::pin::Pin;
use std::sync::{Arc, Condvar, Mutex};
use std::task::{Context, Poll, Waker};
use std::thread;
use std::time::{Duration, Instant};

struct Entry {
    deadline: Instant,
    waker: Waker,
}

// impl Ord for Entry and the other three traits ...

#[derive(Clone)]
pub struct Timers {
    shared: Arc<(Mutex<BinaryHeap<Entry>>, Condvar)>,
}

impl Timers {
    pub fn new() -> Self {
        let shared = Arc::new((Mutex::new(BinaryHeap::new()), Condvar::new()));
        let for_thread = shared.clone();
        thread::spawn(move || {
            let (heap, wakeup) = &*for_thread;
            let mut heap = heap.lock().unwrap();
            loop {
                let now = Instant::now();
                while heap.peek().is_some_and(|entry: &Entry| entry.deadline <= now) {
                    heap.pop().unwrap().waker.wake();
                }
                heap = match heap.peek() {
                    Some(entry) => {
                        let wait = entry.deadline - now;
                        wakeup.wait_timeout(heap, wait).unwrap().0
                    }
                    None => wakeup.wait(heap).unwrap(),
                };
            }
        });
        Timers { shared }
    }

    pub fn sleep(&self, ms: u64) -> Sleep {
        Sleep {
            deadline: Instant::now() + Duration::from_millis(ms),
            timers: self.clone(),
        }
    }
}

pub struct Sleep {
    deadline: Instant,
    timers: Timers,
}

// impl Future for Sleep ...

fn main() {
    let (spawner, queue) = executor();
    let timers = Timers::new();
    let order = Arc::new(Mutex::new(Vec::new()));
    for (id, ms) in [(1, 120), (2, 40), (3, 80)] {
        let (timers, order) = (timers.clone(), order.clone());
        spawner.detach(async move {
            timers.sleep(ms).await;
            order.lock().unwrap().push(id);
        });
    }
    drop(spawner);
    run(queue);
    println!("{:?}", order.lock().unwrap());
}
