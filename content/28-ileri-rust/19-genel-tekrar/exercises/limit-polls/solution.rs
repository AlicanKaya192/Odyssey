use std::future::Future;
use std::pin::{Pin, pin};
use std::task::{Context, Poll, Waker};

struct Yield {
    done: bool,
}

impl Future for Yield {
    type Output = ();

    fn poll(mut self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<()> {
        if self.done {
            return Poll::Ready(());
        }
        self.done = true;
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

struct Limit<F> {
    inner: F,
    left: u32,
}

impl<F: Future> Future for Limit<F> {
    type Output = Option<F::Output>;

    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output> {
        // SAFETY: inner is never moved out, and left is not pinned.
        let this = unsafe { self.get_unchecked_mut() };
        if this.left == 0 {
            return Poll::Ready(None);
        }
        this.left -= 1;
        // SAFETY: self is pinned, so its inner field stays in place too.
        let inner = unsafe { Pin::new_unchecked(&mut this.inner) };
        match inner.poll(cx) {
            Poll::Ready(value) => Poll::Ready(Some(value)),
            Poll::Pending => Poll::Pending,
        }
    }
}

async fn slow(pauses: u32) -> u32 {
    for _ in 0..pauses {
        Yield { done: false }.await;
    }
    pauses
}

fn main() {
    println!("{:?}", block_on(Limit { inner: slow(1), left: 5 }));
    println!("{:?}", block_on(Limit { inner: slow(9), left: 3 }));
}
