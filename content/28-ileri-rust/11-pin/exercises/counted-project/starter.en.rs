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

async fn pause() {
    Yield { done: false }.await;
}

struct Counted<F> {
    inner: F,
    polls: u32,
}

// impl<F: Future> Future for Counted<F> ...

fn main() {
    let mut future = pin!(Counted { inner: pause(), polls: 0 });
    let mut cx = Context::from_waker(Waker::noop());
    while future.as_mut().poll(&mut cx).is_pending() {}
    println!("{}", future.polls);
}
