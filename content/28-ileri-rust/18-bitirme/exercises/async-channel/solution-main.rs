mod rt;

use rt::{Yield, executor, run};
use std::collections::VecDeque;
use std::future::Future;
use std::pin::Pin;
use std::sync::{Arc, Mutex};
use std::task::{Context, Poll, Waker};

struct ChanState<T> {
    items: VecDeque<T>,
    waker: Option<Waker>,
    senders: usize,
}

pub struct ChanSender<T> {
    state: Arc<Mutex<ChanState<T>>>,
}

pub struct ChanReceiver<T> {
    state: Arc<Mutex<ChanState<T>>>,
}

pub fn async_channel<T>() -> (ChanSender<T>, ChanReceiver<T>) {
    let state = ChanState { items: VecDeque::new(), waker: None, senders: 1 };
    let state = Arc::new(Mutex::new(state));
    (ChanSender { state: state.clone() }, ChanReceiver { state })
}

impl<T> ChanSender<T> {
    pub fn send(&self, value: T) {
        let waker = {
            let mut state = self.state.lock().unwrap();
            state.items.push_back(value);
            state.waker.take()
        };
        if let Some(waker) = waker {
            waker.wake();
        }
    }
}

impl<T> Clone for ChanSender<T> {
    fn clone(&self) -> Self {
        self.state.lock().unwrap().senders += 1;
        ChanSender { state: self.state.clone() }
    }
}

impl<T> Drop for ChanSender<T> {
    fn drop(&mut self) {
        let waker = {
            let mut state = self.state.lock().unwrap();
            state.senders -= 1;
            state.waker.take()
        };
        if let Some(waker) = waker {
            waker.wake();
        }
    }
}

impl<T> ChanReceiver<T> {
    pub fn recv(&mut self) -> Recv<'_, T> {
        Recv { receiver: self }
    }
}

pub struct Recv<'a, T> {
    receiver: &'a mut ChanReceiver<T>,
}

impl<T> Future for Recv<'_, T> {
    type Output = Option<T>;

    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Option<T>> {
        let mut state = self.receiver.state.lock().unwrap();
        if let Some(value) = state.items.pop_front() {
            return Poll::Ready(Some(value));
        }
        if state.senders == 0 {
            return Poll::Ready(None);
        }
        state.waker = Some(cx.waker().clone());
        Poll::Pending
    }
}

fn main() {
    let (spawner, queue) = executor();
    let (sender, mut receiver) = async_channel();
    let second = sender.clone();
    spawner.detach(async move {
        sender.send(1);
        Yield { done: false }.await;
        sender.send(2);
    });
    spawner.detach(async move {
        second.send(3);
    });
    spawner.detach(async move {
        let mut total = 0;
        while let Some(value) = receiver.recv().await {
            total += value;
        }
        println!("{total}");
    });
    drop(spawner);
    run(queue);
}
