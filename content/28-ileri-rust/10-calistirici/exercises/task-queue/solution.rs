use std::future::Future;
use std::pin::Pin;
use std::sync::mpsc::{Receiver, Sender, channel};
use std::sync::{Arc, Mutex};
use std::task::{Context, Poll, Wake, Waker};

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

type BoxFuture = Pin<Box<dyn Future<Output = ()> + Send>>;

struct Task {
    future: Mutex<Option<BoxFuture>>,
    queue: Sender<Arc<Task>>,
}

impl Wake for Task {
    fn wake(self: Arc<Self>) {
        let queue = self.queue.clone();
        let _ = queue.send(self);
    }
}

fn spawn<F>(queue: &Sender<Arc<Task>>, future: F)
where
    F: Future<Output = ()> + Send + 'static,
{
    let task = Task {
        future: Mutex::new(Some(Box::pin(future))),
        queue: queue.clone(),
    };
    queue.send(Arc::new(task)).unwrap();
}

fn run(queue: Receiver<Arc<Task>>) {
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

async fn worker(name: &'static str) {
    for round in 0..2 {
        println!("{name} {round}");
        Yield { done: false }.await;
    }
}

fn main() {
    let (sender, receiver) = channel();
    spawn(&sender, worker("a"));
    spawn(&sender, worker("b"));
    drop(sender);
    run(receiver);
}
