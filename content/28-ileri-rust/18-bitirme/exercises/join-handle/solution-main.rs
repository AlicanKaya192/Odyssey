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

impl<T> Future for JoinHandle<T> {
    type Output = T;

    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<T> {
        let mut state = self.state.lock().unwrap();
        if let Some(value) = state.value.take() {
            return Poll::Ready(value);
        }
        state.waker = Some(cx.waker().clone());
        Poll::Pending
    }
}

pub fn spawn<F>(spawner: &Spawner, future: F) -> JoinHandle<F::Output>
where
    F: Future + Send + 'static,
    F::Output: Send + 'static,
{
    let state = Arc::new(Mutex::new(JoinState { value: None, waker: None }));
    let shared = state.clone();
    spawner.detach(async move {
        let value = future.await;
        let waker = {
            let mut state = shared.lock().unwrap();
            state.value = Some(value);
            state.waker.take()
        };
        if let Some(waker) = waker {
            waker.wake();
        }
    });
    JoinHandle { state }
}

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
