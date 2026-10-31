use std::future::Future;
use std::pin::{Pin, pin};
use std::sync::{Arc, Mutex};
use std::task::{Context, Poll, Wake, Waker};
use std::thread::{self, Thread};
use std::time::Duration;

struct ThreadWaker(Thread);

impl Wake for ThreadWaker {
    fn wake(self: Arc<Self>) {
        self.0.unpark();
    }
}

fn block_on<F: Future>(future: F) -> F::Output {
    let mut future = pin!(future);
    let waker = Waker::from(Arc::new(ThreadWaker(thread::current())));
    let mut cx = Context::from_waker(&waker);
    loop {
        match future.as_mut().poll(&mut cx) {
            Poll::Ready(value) => return value,
            Poll::Pending => thread::park(),
        }
    }
}

struct State<T> {
    value: Option<T>,
    waker: Option<Waker>,
}

struct OneSender<T> {
    state: Arc<Mutex<State<T>>>,
}

struct OneReceiver<T> {
    state: Arc<Mutex<State<T>>>,
}

fn oneshot<T>() -> (OneSender<T>, OneReceiver<T>) {
    let state = Arc::new(Mutex::new(State { value: None, waker: None }));
    (OneSender { state: state.clone() }, OneReceiver { state })
}

// impl<T> OneSender<T> { fn send(self, value: T) ... }
// impl<T> Future for OneReceiver<T> ...

fn main() {
    let (sender, receiver) = oneshot();
    thread::spawn(move || {
        thread::sleep(Duration::from_millis(20));
        sender.send(7);
    });
    println!("{}", block_on(receiver));
}
