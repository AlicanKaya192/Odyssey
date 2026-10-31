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

// impl<A: Future, B: Future> Future for Join<A, B> ...

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
