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

struct Join<A: Future, B: Future> {
    a: A,
    b: B,
    a_out: Option<A::Output>,
    b_out: Option<B::Output>,
    a_done: bool,
    b_done: bool,
}

impl<A: Future, B: Future> Future for Join<A, B> {
    type Output = (A::Output, B::Output);

    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output> {
        // SAFETY: a and b are never moved out; the outputs are not pinned.
        let this = unsafe { self.get_unchecked_mut() };
        if !this.a_done {
            // SAFETY: self is pinned, so a stays in place too.
            let a = unsafe { Pin::new_unchecked(&mut this.a) };
            if let Poll::Ready(value) = a.poll(cx) {
                this.a_out = Some(value);
                this.a_done = true;
            }
        }
        if !this.b_done {
            // SAFETY: self is pinned, so b stays in place too.
            let b = unsafe { Pin::new_unchecked(&mut this.b) };
            if let Poll::Ready(value) = b.poll(cx) {
                this.b_out = Some(value);
                this.b_done = true;
            }
        }
        if this.a_done && this.b_done {
            let a = this.a_out.take().expect("polled after completion");
            let b = this.b_out.take().expect("polled after completion");
            Poll::Ready((a, b))
        } else {
            Poll::Pending
        }
    }
}

async fn after(pauses: u32, value: u32) -> u32 {
    for _ in 0..pauses {
        pause().await;
    }
    value
}

fn main() {
    let join = Join {
        a: after(2, 10),
        b: after(0, 20),
        a_out: None,
        b_out: None,
        a_done: false,
        b_done: false,
    };
    println!("{:?}", block_on(join));
}
