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

// impl<A, B> Future for Select<A, B> ...

fn main() {
    let never = std::future::pending::<u32>();
    let race = Select { a: never, b: std::future::ready("won") };
    println!("{:?}", block_on(race));
}
