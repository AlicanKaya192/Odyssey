use std::future::Future;
use std::pin::{Pin, pin};
use std::task::{Context, Poll, Waker};

#[derive(Debug, PartialEq)]
enum Either<A, B> {
    Left(A),
    Right(B),
}

struct Select<A, B> {
    a: A,
    b: B,
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

impl<A, B> Future for Select<A, B>
where
    A: Future + Unpin,
    B: Future + Unpin,
{
    type Output = Either<A::Output, B::Output>;

    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output> {
        let this = self.get_mut();
        if let Poll::Ready(value) = Pin::new(&mut this.a).poll(cx) {
            return Poll::Ready(Either::Left(value));
        }
        if let Poll::Ready(value) = Pin::new(&mut this.b).poll(cx) {
            return Poll::Ready(Either::Right(value));
        }
        Poll::Pending
    }
}

fn main() {
    let never = std::future::pending::<u32>();
    let race = Select { a: never, b: std::future::ready("won") };
    println!("{:?}", block_on(race));
}
