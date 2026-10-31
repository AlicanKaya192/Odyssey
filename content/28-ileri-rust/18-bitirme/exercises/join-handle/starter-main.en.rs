mod rt;

use rt::{Spawner, Yield, executor, run};
use std::future::Future;
use std::pin::Pin;
use std::sync::{Arc, Mutex};
use std::task::{Context, Poll, Waker};

struct JoinState<T> {
    value: Option<T>,
    waker: Option<Waker>,
}

pub struct JoinHandle<T> {
    state: Arc<Mutex<JoinState<T>>>,
}

// impl<T> Future for JoinHandle<T> ...
// pub fn spawn<F>(spawner: &Spawner, future: F) -> JoinHandle<F::Output> ...

fn main() {
    let (spawner, queue) = executor();
    let first = spawn(&spawner, async {
        Yield { done: false }.await;
        2
    });
    let second = spawn(&spawner, async { String::from("three") });
    spawner.detach(async move {
        let text = second.await;
        let number = first.await;
        println!("{text} {number}");
    });
    drop(spawner);
    run(queue);
}
