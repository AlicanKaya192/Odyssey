use std::future::Future;
use std::pin::{Pin, pin};
use std::task::{Context, Poll, Waker};

struct Task {
    left: u32,
    value: u32,
    finished: bool,
}

impl Task {
    fn new(left: u32, value: u32) -> Self {
        Task { left, value, finished: false }
    }
}

impl Future for Task {
    type Output = u32;

    fn poll(mut self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<u32> {
        assert!(!self.finished, "polled after completion");
        if self.left == 0 {
            self.finished = true;
            return Poll::Ready(self.value);
        }
        self.left -= 1;
        cx.waker().wake_by_ref();
        Poll::Pending
    }
}

struct Join2<A, B> {
    a: A,
    b: B,
    a_out: Option<u32>,
    b_out: Option<u32>,
}

fn block_on<F: Future>(future: F) -> F::Output {
    let mut future = pin!(future);
    let mut cx = Context::from_waker(Waker::noop());
    loop {
        if let Poll::Ready(value) = future.as_mut().poll(&mut cx) {
            return value;
        }
    }
}

// impl<A, B> Future for Join2<A, B> ...

fn main() {
    let join = Join2 { a: Task::new(2, 10), b: Task::new(0, 20), a_out: None, b_out: None };
    println!("{:?}", block_on(join));
}
