# Capstone Project: A Small Async Runtime

In this module we saw `unsafe`, memory layout, atomics, `Future`, wakers and `Pin`. Now we combine them all in something real: our own small **async runtime**. We will write small versions of the parts at the core of libraries like `tokio`:

| Part | What it does | From which section |
|---|---|---|
| Ring buffer | A lock-free, fixed-capacity queue | `unsafe`, `MaybeUninit`, atomics |
| Executor | Polls tasks from a queue | `Future`, `Wake` |
| `JoinHandle` | Awaits a task's result | Wakers, `Arc`, `Mutex` |
| Channel | Messages between tasks | Wakers, `Drop` |
| Timer | Thousands of deadlines on one branch | `BinaryHeap`, `Condvar` |

## Ring buffer: a lock-free queue

With one producer and one consumer, no lock is needed. The producer only writes `tail`, and the consumer only writes `head`. Neither is ever reset: `tail - head` gives how many items there are, and `index % N` gives the slot.

```rust
use std::cell::UnsafeCell;
use std::mem::MaybeUninit;
use std::sync::atomic::{AtomicUsize, Ordering};
use std::thread;

pub struct Ring<T, const N: usize> {
    slots: [UnsafeCell<MaybeUninit<T>>; N],
    head: AtomicUsize,
    tail: AtomicUsize,
}

// SAFETY: head and tail hand each slot between one producer and one consumer.
unsafe impl<T: Send, const N: usize> Sync for Ring<T, N> {}

impl<T, const N: usize> Ring<T, N> {
    pub fn new() -> Self {
        Ring {
            slots: std::array::from_fn(|_| UnsafeCell::new(MaybeUninit::uninit())),
            head: AtomicUsize::new(0),
            tail: AtomicUsize::new(0),
        }
    }

    pub fn split(&mut self) -> (Producer<'_, T, N>, Consumer<'_, T, N>) {
        (Producer { ring: self }, Consumer { ring: self })
    }
}

pub struct Producer<'a, T, const N: usize> {
    ring: &'a Ring<T, N>,
}

pub struct Consumer<'a, T, const N: usize> {
    ring: &'a Ring<T, N>,
}

impl<T, const N: usize> Producer<'_, T, N> {
    pub fn push(&mut self, value: T) -> Result<(), T> {
        let tail = self.ring.tail.load(Ordering::Relaxed);
        let head = self.ring.head.load(Ordering::Acquire);
        if tail - head == N {
            return Err(value);
        }
        let slot = self.ring.slots[tail % N].get();
        // SAFETY: this slot is empty, and only this producer writes.
        unsafe { (*slot).write(value) };
        self.ring.tail.store(tail + 1, Ordering::Release);
        Ok(())
    }
}

impl<T, const N: usize> Consumer<'_, T, N> {
    pub fn pop(&mut self) -> Option<T> {
        let head = self.ring.head.load(Ordering::Relaxed);
        let tail = self.ring.tail.load(Ordering::Acquire);
        if head == tail {
            return None;
        }
        let slot = self.ring.slots[head % N].get();
        // SAFETY: Acquire saw this slot written, and only this consumer reads.
        let value = unsafe { (*slot).assume_init_read() };
        self.ring.head.store(head + 1, Ordering::Release);
        Some(value)
    }
}

impl<T, const N: usize> Drop for Ring<T, N> {
    fn drop(&mut self) {
        let (head, tail) = (*self.head.get_mut(), *self.tail.get_mut());
        for index in head..tail {
            // SAFETY: slots from head to tail hold values nobody has read.
            unsafe { self.slots[index % N].get_mut().assume_init_drop() };
        }
    }
}

fn main() {
    let mut ring = Ring::<u32, 16>::new();
    let (mut producer, mut consumer) = ring.split();
    let sum = thread::scope(|s| {
        s.spawn(move || {
            for value in 1..=100_000 {
                let mut value = value;
                while let Err(back) = producer.push(value) {
                    value = back;
                    thread::yield_now();
                }
            }
        });
        let mut sum = 0u64;
        let mut seen = 0;
        while seen < 100_000 {
            match consumer.pop() {
                Some(value) => {
                    sum += u64::from(value);
                    seen += 1;
                }
                None => thread::yield_now(),
            }
        }
        sum
    });
    println!("{sum}");
}
```

```text
5000050000
```

Much of the module is in this code:

- `MaybeUninit`: an empty slot has no `T` yet; we reserve room without building one.
- `UnsafeCell`: the legal way to write through `&self`.
- `Acquire` and `Release`: when the producer writes `tail` with `Release`, the value written so far becomes visible to the consumer reading with `Acquire`.
- `Drop`: `MaybeUninit` does not drop its contents itself; we drop the unread ones.

The real design decision is in `split`. The condition "one producer, one consumer" is required for `Ring` to be correct. Instead of writing that in documentation, we wrote it into the types: `split(&mut self)` cannot be called again while its borrow lasts, `Producer` cannot be copied, and `push` takes `&mut self`. If two branches try to use the same producer, it does not compile. **Keeping `unsafe`'s promise through types** is the most important idea of this module.

## Executor

The same executor as in section 10, made clonable under the name `Spawner`:

```rust
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
```

`detach` starts a task and leaves it, with no result. `run` works until the queue closes.

## JoinHandle: a task with a result

If we want a task's result, we must have it written to a shared state and wake whoever waits:

```rust
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
```

Note the trick: `spawn` wraps the given future inside another `async move`. The wrapper knows where the result goes, and the real future need not know.

## Channel

For messages between tasks, the queue and the waker sit behind the same lock:

```rust
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
```

The subtle point is the last sender: `Drop` counts it and wakes the waiting receiver. Without this, the receiver would stay at `Pending` forever, the same "silently hanging" mistake as in section 10.

## Timer

In section 10 each `Timer` opened a branch. Ten thousand timers would mean ten thousand branches, exactly what we are escaping. The solution is one branch and a sorted heap (`BinaryHeap`):

```rust
struct Entry {
    deadline: Instant,
    waker: Waker,
}

impl PartialEq for Entry {
    fn eq(&self, other: &Self) -> bool {
        self.deadline == other.deadline
    }
}

impl Eq for Entry {}

impl PartialOrd for Entry {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for Entry {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        other.deadline.cmp(&self.deadline)
    }
}
```

`BinaryHeap` puts the largest on top, and we need the nearest deadline. So `Ord` was written reversed: `other` against `self`.

```rust
#[derive(Clone)]
pub struct Timers {
    shared: Arc<(Mutex<BinaryHeap<Entry>>, Condvar)>,
}

impl Timers {
    pub fn new() -> Self {
        let shared = Arc::new((Mutex::new(BinaryHeap::new()), Condvar::new()));
        let for_thread = shared.clone();
        thread::spawn(move || {
            let (heap, wakeup) = &*for_thread;
            let mut heap = heap.lock().unwrap();
            loop {
                let now = Instant::now();
                while heap.peek().is_some_and(|entry: &Entry| entry.deadline <= now) {
                    heap.pop().unwrap().waker.wake();
                }
                heap = match heap.peek() {
                    Some(entry) => {
                        let wait = entry.deadline - now;
                        wakeup.wait_timeout(heap, wait).unwrap().0
                    }
                    None => wakeup.wait(heap).unwrap(),
                };
            }
        });
        Timers { shared }
    }

    pub fn sleep(&self, ms: u64) -> Sleep {
        Sleep {
            deadline: Instant::now() + Duration::from_millis(ms),
            timers: self.clone(),
        }
    }
}

pub struct Sleep {
    deadline: Instant,
    timers: Timers,
}

impl Future for Sleep {
    type Output = ();

    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<()> {
        if Instant::now() >= self.deadline {
            return Poll::Ready(());
        }
        let (heap, wakeup) = &*self.timers.shared;
        let waker = cx.waker().clone();
        heap.lock().unwrap().push(Entry { deadline: self.deadline, waker });
        wakeup.notify_one();
        Poll::Pending
    }
}
```

The branch sleeps until the nearest deadline. A new `Sleep` may be nearer, so on each addition we wake the branch with `notify_one`, and it recalculates.

## All together

```rust
async fn fetch(timers: Timers, out: ChanSender<u32>, id: u32, ms: u64) {
    timers.sleep(ms).await;
    out.send(id);
}

fn main() {
    let (spawner, queue) = executor();
    let timers = Timers::new();
    let (sender, mut receiver) = async_channel();
    let start = Instant::now();

    spawner.detach(fetch(timers.clone(), sender.clone(), 1, 150));
    spawner.detach(fetch(timers.clone(), sender.clone(), 2, 50));
    spawner.detach(fetch(timers.clone(), sender, 3, 100));

    let collect = spawn(&spawner, async move {
        let mut seen = Vec::new();
        while let Some(id) = receiver.recv().await {
            seen.push(id);
        }
        seen
    });
    spawner.detach(async move {
        println!("{:?}", collect.await);
        println!("under 300 ms: {}", start.elapsed() < Duration::from_millis(300));
    });

    drop(spawner);
    run(queue);
}
```

```text
[2, 3, 1]
under 300 ms: true
```

Three tasks waited together on one branch, the finished ones wrote to the channel, and another task collected. The order is deadline order, not start order. The total of 300 milliseconds of waiting took less, and there are only two branches: the executor and the timer.

## Summary

You now hold the skeleton of a real runtime. What is missing are big parts but not new ideas: the operating system's event mechanism for networks, several worker branches, and work stealing. This project means you now know what happens in the layers below when you write an `async fn`.
