# Bitirme Projesi: Küçük Bir Async Çalışma Ortamı

Bu modülde `unsafe`, bellek düzeni, atomikler, `Future`, waker ve `Pin` gördük. Şimdi hepsini gerçek bir şeyde birleştiriyoruz: Kendi küçük **async çalışma ortamımız** (runtime). `tokio` gibi kütüphanelerin çekirdeğinde olan parçaların küçük hâllerini yazacağız:

| Parça | Ne yapar | Hangi bölümden |
|---|---|---|
| Halka tampon | Kilitsiz, sabit kapasiteli kuyruk | `unsafe`, `MaybeUninit`, atomikler |
| Çalıştırıcı | Görevleri kuyruktan yoklar | `Future`, `Wake` |
| `JoinHandle` | Görevin sonucunu bekler | Waker, `Arc`, `Mutex` |
| Kanal | Görevler arası mesaj | Waker, `Drop` |
| Zamanlayıcı | Tek kolda binlerce süre | `BinaryHeap`, `Condvar` |

## Halka tampon: Kilitsiz kuyruk

Tek üretici ve tek tüketici varsa kilit gerekmez. Üretici yalnızca `tail`'i, tüketici yalnızca `head`'i yazar. İkisi hiç sıfırlanmaz: `tail - head` kaç öğe olduğunu, `index % N` yuvayı verir.

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

Bu kodda modülün çoğu var:

- `MaybeUninit`: Boş yuvada henüz `T` yok, kurmadan yer ayırıyoruz.
- `UnsafeCell`: `&self` üstünden yazmanın yasal yolu.
- `Acquire` ve `Release`: Üretici `tail`'i `Release` ile yazınca o ana kadar yazılan değer, `Acquire` ile okuyan tüketiciye görünür.
- `Drop`: `MaybeUninit` içindekini kendisi düşürmez; okunmamışları biz düşürürüz.

Asıl tasarım kararı `split`'te. "Tek üretici, tek tüketici" şartı `Ring`'in doğruluğu için gerekli. Bunu belgeye yazmak yerine türe yazdık: `split(&mut self)` ödünç sürdüğü sürece yeniden çağrılamaz, `Producer` kopyalanamaz, `push` da `&mut self` ister. İki kol aynı üreticiyi kullanmaya kalkarsa derlenmez. **`unsafe`'in sözünü türle tutturmak** bu modülün en önemli fikridir.

## Çalıştırıcı

10. bölümdeki çalıştırıcının aynısı, `Spawner` adıyla klonlanabilir hâle getirdik:

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

`detach` görevi başlatıp bırakır, sonucu yoktur. `run` kuyruk kapanana kadar çalışır.

## JoinHandle: Sonucu olan görev

Görevin sonucunu istiyorsak onu paylaşılan bir duruma yazdırmalı ve bekleyeni uyandırmalıyız:

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

Hileye dikkat: `spawn`, verilen future'ı başka bir `async move` içine sarar. Sonucun nereye gideceğini sarmalayıcı bilir, asıl future bilmek zorunda kalmaz.

## Kanal

Görevler arası mesaj için kuyruk ve waker aynı kilidin arkasında durur:

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

İnce nokta son gönderici: `Drop` onu sayar ve bekleyen alıcıyı uyandırır. Bunu yazmasaydık alıcı `Pending`'de sonsuza kadar kalırdı, yani 10. bölümdeki "sessizce asılı kalan" hatanın aynısı olurdu.

## Zamanlayıcı

10. bölümde her `Timer` bir kol açıyordu. On bin zamanlayıcıda on bin kol, tam da kaçtığımız şey. Çözüm tek kol ve sıralı bir yığın (`BinaryHeap`):

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

`BinaryHeap` en büyüğü üste koyar, bize en yakın süre lazım. O yüzden `Ord` ters yazıldı: `other` ile `self`.

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

Kol en yakın süreye kadar uyur. Yeni bir `Sleep` daha yakın olabilir, bu yüzden her eklemede `notify_one` ile kolu uyandırırız, o da yeniden hesaplar.

## Hepsi birlikte

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

Üç görev tek kolda birlikte bekledi, biten kanala yazdı, başka bir görev topladı. Sıra başlatma sırası değil, süre sırası. Toplam 300 milisaniyelik bekleme bundan kısa sürdü ve kol sayısı yalnızca iki: Çalıştırıcı ve zamanlayıcı.

## Özet

Elinde artık gerçek çalışma ortamının iskeleti var. Eksik olanlar büyük parçalar ama yeni fikir değil: Ağ için işletim sisteminin olay mekanizması, birden çok işçi kol ve iş çalma. Bu proje, bir `async fn` yazdığında alttaki katmanlarda ne olduğunu artık bildiğin anlamına geliyor.
