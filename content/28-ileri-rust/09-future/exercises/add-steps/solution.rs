use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Poll, Waker};

struct Later {
    value: u32,
    waited: bool,
}

impl Later {
    fn new(value: u32) -> Self {
        Later { value, waited: false }
    }
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

enum AddSteps {
    First(Later),
    Second(u32, Later),
    Done,
}

impl Future for AddSteps {
    type Output = u32;

    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<u32> {
        let this = self.get_mut();
        loop {
            match this {
                AddSteps::First(later) => {
                    let Poll::Ready(a) = Pin::new(later).poll(cx) else {
                        return Poll::Pending;
                    };
                    *this = AddSteps::Second(a, Later::new(a * 2));
                }
                AddSteps::Second(a, later) => {
                    let a = *a;
                    let Poll::Ready(b) = Pin::new(later).poll(cx) else {
                        return Poll::Pending;
                    };
                    *this = AddSteps::Done;
                    return Poll::Ready(a + b);
                }
                AddSteps::Done => panic!("polled after completion"),
            }
        }
    }
}

fn main() {
    let mut future = AddSteps::First(Later::new(5));
    let mut cx = Context::from_waker(Waker::noop());
    for _ in 0..3 {
        println!("{:?}", Pin::new(&mut future).poll(&mut cx));
    }
}
