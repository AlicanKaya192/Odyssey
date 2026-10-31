use std::future::Future;
use std::pin::{Pin, pin};
use std::task::{Context, Poll, Waker};

struct Countdown {
    left: u32,
}

impl Future for Countdown {
    type Output = &'static str;

    fn poll(mut self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output> {
        if self.left == 0 {
            return Poll::Ready("done");
        }
        self.left -= 1;
        cx.waker().wake_by_ref();
        Poll::Pending
    }
}

// fn block_on<F: Future>(future: F) -> F::Output ...

fn main() {
    println!("{}", block_on(Countdown { left: 3 }));
    println!("{}", block_on(async { 40 + 2 }));
}
