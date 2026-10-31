use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Poll, Waker};

struct ReadyAfter {
    left: u32,
    value: u32,
}

impl Future for ReadyAfter {
    type Output = u32;

    fn poll(mut self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<u32> {
        if self.left == 0 {
            return Poll::Ready(self.value);
        }
        self.left -= 1;
        cx.waker().wake_by_ref();
        Poll::Pending
    }
}

fn main() {
    let mut future = ReadyAfter { left: 1, value: 5 };
    let mut cx = Context::from_waker(Waker::noop());
    println!("{:?}", Pin::new(&mut future).poll(&mut cx));
    println!("{:?}", Pin::new(&mut future).poll(&mut cx));
}
