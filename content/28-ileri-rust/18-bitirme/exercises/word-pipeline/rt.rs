use std::collections::VecDeque;
use std::future::Future;
use std::pin::Pin;
use std::sync::mpsc::{Receiver, Sender, channel};
use std::sync::{Arc, Mutex};
use std::task::{Context, Poll, Wake, Waker};

type BoxFuture = Pin<Box<dyn Future<Output = ()> + Send>>;

pub struct Task {
    future: Mutex<Option<BoxFuture>>,
    queue: Sender<Arc<Task>>,
}

impl Wake for Task {
    fn wake(self: Arc<Self>) {
        let queue = self.queue.clone();
        let _ = queue.send(self);
    }
}

#[derive(Clone)]
pub struct Spawner {
    queue: Sender<Arc<Task>>,
}

impl Spawner {
    pub fn detach<F>(&self, future: F)
    where
        F: Future<Output = ()> + Send + 'static,
    {
        let task = Task {
            future: Mutex::new(Some(Box::pin(future))),
            queue: self.queue.clone(),
        };
        self.queue.send(Arc::new(task)).unwrap();
    }
}

pub fn executor() -> (Spawner, Receiver<Arc<Task>>) {
    let (queue, receiver) = channel();
    (Spawner { queue }, receiver)
}

pub fn run(queue: Receiver<Arc<Task>>) {
    while let Ok(task) = queue.recv() {
        let mut slot = task.future.lock().unwrap();
        if let Some(future) = slot.as_mut() {
            let waker = Waker::from(task.clone());
            let mut cx = Context::from_waker(&waker);
            if future.as_mut().poll(&mut cx).is_ready() {
                *slot = None;
            }
        }
    }
}

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
