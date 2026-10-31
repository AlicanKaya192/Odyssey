use std::future::Future;
use std::pin::{Pin, pin};
use std::task::{Context, Poll, Waker};

struct Later {
    value: u32,
    waited: bool,
}

impl Future for Later {
    type Output = u32;

    fn poll(mut self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<u32> {
        if self.waited {
            return Poll::Ready(self.value);
        }
        self.waited = true;
        cx.waker().wake_by_ref();
        Poll::Pending
    }
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

// async fn sum_later(values: Vec<u32>) -> u32 ...

fn main() {
    println!("{}", block_on(sum_later(vec![1, 2, 3])));
}
