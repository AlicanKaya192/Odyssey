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

fn block_on<F: Future>(future: F) -> F::Output {
    let mut future = pin!(future);
    let mut cx = Context::from_waker(Waker::noop());
    loop {
        if let Poll::Ready(value) = future.as_mut().poll(&mut cx) {
            return value;
        }
    }
}

struct Map<F, C> {
    inner: F,
    func: Option<C>,
}

impl<F, C, R> Future for Map<F, C>
where
    F: Future,
    C: FnOnce(F::Output) -> R,
{
    type Output = R;

    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<R> {
        // SAFETY: inner is never moved out, and func is not pinned.
        let this = unsafe { self.get_unchecked_mut() };
        // SAFETY: self is pinned, so its inner field stays in place too.
        let inner = unsafe { Pin::new_unchecked(&mut this.inner) };
        match inner.poll(cx) {
            Poll::Ready(value) => {
                let func = this.func.take().expect("polled after completion");
                Poll::Ready(func(value))
            }
            Poll::Pending => Poll::Pending,
        }
    }
}

async fn seven() -> u32 {
    pause().await;
    7
}

fn main() {
    let future = Map { inner: seven(), func: Some(|n: u32| n + 1) };
    println!("{}", block_on(future));
}
