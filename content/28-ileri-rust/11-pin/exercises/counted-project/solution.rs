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

impl<F: Future> Future for Counted<F> {
    type Output = F::Output;

    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<F::Output> {
        // SAFETY: inner is never moved out of self.
        let this = unsafe { self.get_unchecked_mut() };
        this.polls += 1;
        // SAFETY: self is pinned, so its inner field stays in place too.
        let inner = unsafe { Pin::new_unchecked(&mut this.inner) };
        inner.poll(cx)
    }
}

fn main() {
    let mut future = pin!(Counted { inner: pause(), polls: 0 });
    let mut cx = Context::from_waker(Waker::noop());
    while future.as_mut().poll(&mut cx).is_pending() {}
    println!("{}", future.polls);
}
