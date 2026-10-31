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

fn finishes_at_once<F: Future>(future: F) -> bool {
    let future = pin!(future);
    let mut cx = Context::from_waker(Waker::noop());
    future.poll(&mut cx).is_ready()
}

fn main() {
    println!("{}", finishes_at_once(async { 1 }));
    println!("{}", finishes_at_once(pause()));
}
