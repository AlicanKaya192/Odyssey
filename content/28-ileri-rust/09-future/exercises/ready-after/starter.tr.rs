use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Poll, Waker};

struct ReadyAfter {
    left: u32,
    value: u32,
}

// impl Future for ReadyAfter ...

fn main() {
    let mut future = ReadyAfter { left: 1, value: 5 };
    let mut cx = Context::from_waker(Waker::noop());
    println!("{:?}", Pin::new(&mut future).poll(&mut cx));
    println!("{:?}", Pin::new(&mut future).poll(&mut cx));
}
