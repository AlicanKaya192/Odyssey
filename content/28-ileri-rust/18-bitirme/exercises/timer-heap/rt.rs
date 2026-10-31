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

pub struct Yield {
    pub done: bool,
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
