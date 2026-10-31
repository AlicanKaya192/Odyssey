use std::future::Future;
use std::pin::{Pin, pin};
use std::sync::{Arc, Mutex};
use std::task::{Context, Poll, Wake, Waker};
use std::thread::{self, Thread};
use std::time::Duration;

struct Shared {
    done: bool,
    waker: Option<Waker>,
}

struct Timer {
    shared: Arc<Mutex<Shared>>,
}

impl Timer {
    fn new(ms: u64) -> Self {
        let shared = Arc::new(Mutex::new(Shared { done: false, waker: None }));
        let for_thread = shared.clone();
        thread::spawn(move || {
            thread::sleep(Duration::from_millis(ms));
            let waker = {
                let mut state = for_thread.lock().unwrap();
                state.done = true;
                state.waker.take()
            };
            if let Some(waker) = waker {
                waker.wake();
            }
        });
        Timer { shared }
    }
}

impl Future for Timer {
    type Output = ();

    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<()> {
        let mut state = self.shared.lock().unwrap();
        if state.done {
            return Poll::Ready(());
        }
        state.waker = Some(cx.waker().clone());
        Poll::Pending
    }
}

// struct ThreadWaker ...
// impl Wake for ThreadWaker ...
// fn block_on<F: Future>(future: F) -> F::Output ...

fn main() {
    block_on(Timer::new(20));
    println!("{}", block_on(async { 40 + 2 }));
}
