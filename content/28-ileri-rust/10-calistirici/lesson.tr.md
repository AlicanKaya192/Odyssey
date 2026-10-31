# Kendi Async Çalıştırıcımız

Geçen bölümde `block_on` boşa dönüyordu ve "gerçek çalıştırıcı uyur" demiştik. Şimdi onu yazıyoruz: Önce uyuyan bir `block_on`, sonra birçok işi birlikte yürüten küçük bir çalıştırıcı.

## Önce sorunu ölçelim

Gerçekten bekleyen bir future lazım. `Timer`, arkada bir kol açar, süre dolunca işi bitmiş sayar. (Kodunu birazdan okuyacağız.) Boşa dönen yöntemle 50 milisaniyelik bekleme:

```rust
fn spin_polls<F: Future>(future: F) -> u64 {
    let mut future = pin!(future);
    let mut cx = Context::from_waker(Waker::noop());
    let mut polls = 0;
    loop {
        polls += 1;
        if future.as_mut().poll(&mut cx).is_ready() {
            return polls;
        }
    }
}

fn main() {
    println!("over 1000 polls: {}", spin_polls(Timer::new(50)) > 1000);
}
```

```text
over 1000 polls: true
```

Hiçbir şey olmayan bir bekleyişte binlerce kez sorduk. İşlemci bu süre boyunca boşuna tam yükte çalıştı. İstediğimiz: Sor, cevap `Pending` ise uyu, biri uyandırınca yeniden sor.

## Waker: "Yeniden sor" haberi

Geçen bölümde `Waker::noop()` kullandık, haber hiçbir yere gitmiyordu. Haberin gerçekten bir şey yapması için `Wake` trait'i var. Bir tür yazarız, `Wake` uygularız, `Waker::from` ile waker'a çeviririz:

```rust
use std::future::Future;
use std::pin::pin;
use std::sync::Arc;
use std::task::{Context, Poll, Wake, Waker};
use std::thread::{self, Thread};

struct ThreadWaker(Thread);

impl Wake for ThreadWaker {
    fn wake(self: Arc<Self>) {
        self.0.unpark();
    }
}

fn block_on<F: Future>(future: F) -> F::Output {
    let mut future = pin!(future);
    let waker = Waker::from(Arc::new(ThreadWaker(thread::current())));
    let mut cx = Context::from_waker(&waker);
    loop {
        match future.as_mut().poll(&mut cx) {
            Poll::Ready(value) => return value,
            Poll::Pending => thread::park(),
        }
    }
}

fn main() {
    println!("{}", block_on(async { 40 + 2 }));
}
```

```text
42
```

Parça parça:

- `ThreadWaker(Thread)`: Uyandırılacak kolun kimliğini tutar. `thread::current()` o anki kolu verir.
- `wake(self: Arc<Self>)`: Haber gelince `unpark` ile kolu uyandırır. `Arc` şart, çünkü waker kopyalanıp kollar arasında gezer.
- `thread::park()`: Kolu `unpark` gelene kadar uyutur, işlemci boşalır.

Ölçelim:

```rust
fn counted_block_on<F: Future>(future: F) -> u32 {
    let mut future = pin!(future);
    let waker = Waker::from(Arc::new(ThreadWaker(thread::current())));
    let mut cx = Context::from_waker(&waker);
    let mut polls = 0;
    loop {
        polls += 1;
        match future.as_mut().poll(&mut cx) {
            Poll::Ready(_) => return polls,
            Poll::Pending => thread::park(),
        }
    }
}

fn main() {
    println!("polls: {}", counted_block_on(Timer::new(50)));
}
```

```text
polls: 2
```

Binlerce yerine iki yoklama: Biri başta, biri haber gelince.

`park` çağrısı sebepsiz yere de dönebilir (belgesi böyle söylüyor). Sorun değil, çünkü döngüdeyiz: Yeniden yoklarız, future hâlâ `Pending` der, yeniden uyuruz.

Peki haber tam `poll` ile `park` arasında gelirse kaybolur mu? Hayır. `unpark` bir jeton bırakır; sonraki `park` jetonu görüp hemen döner:

```rust
use std::thread;

fn main() {
    thread::current().unpark();
    thread::park();
    println!("park returned at once");
}
```

```text
park returned at once
```

## Haberi veren taraf: Timer

Waker'ı saklamak future'ın işidir. Asıl işi yapan (burada arkadaki kol), bitince saklanan waker'ı çağırır:

```rust
use std::future::Future;
use std::pin::{Pin, pin};
use std::sync::{Arc, Mutex};
use std::task::{Context, Poll, Wake, Waker};
use std::thread::{self, Thread};
use std::time::Duration;

struct Shared {
    done: bool,
    waker: Option<Waker>,
}

struct Timer {
    shared: Arc<Mutex<Shared>>,
}

impl Timer {
    fn new(ms: u64) -> Self {
        let shared = Arc::new(Mutex::new(Shared { done: false, waker: None }));
        let for_thread = shared.clone();
        thread::spawn(move || {
            thread::sleep(Duration::from_millis(ms));
            let waker = {
                let mut state = for_thread.lock().unwrap();
                state.done = true;
                state.waker.take()
            };
            if let Some(waker) = waker {
                waker.wake();
            }
        });
        Timer { shared }
    }
}

impl Future for Timer {
    type Output = ();

    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<()> {
        let mut state = self.shared.lock().unwrap();
        if state.done {
            return Poll::Ready(());
        }
        state.waker = Some(cx.waker().clone());
        Poll::Pending
    }
}

fn main() {
    block_on(Timer::new(20));
    println!("timer finished");
}
```

```text
timer finished
```

Dikkat edilecek üç nokta:

- `poll` waker'ı **her çağrıda** yeniden saklar. Geçerli olan son yoklamanın waker'ıdır; future başka bir göreve geçmiş olabilir.
- Durum kontrolü ve waker'ı saklamak aynı kilit altındadır. Araya girse kol `done` yazıp henüz saklanmamış waker'ı bulamazdı ve haber kaybolurdu.
- Kol, waker'ı kilitten çıkarıp **kilit bırakıldıktan sonra** uyandırır. Uyanan iş kilidi beklemesin diye.

## Sözleşmeyi çiğnersek

Geçen bölümde söz vermiştik. Bu future ikinci yoklamada biter ama hiç haber vermez:

```rust
struct Forgetful {
    asked: bool,
}

impl Future for Forgetful {
    type Output = ();

    fn poll(mut self: Pin<&mut Self>, _cx: &mut Context<'_>) -> Poll<()> {
        if self.asked {
            return Poll::Ready(());
        }
        self.asked = true;
        Poll::Pending
    }
}

fn finishes_in<F: Future>(future: F, limit: Duration) -> bool {
    let mut future = pin!(future);
    let waker = Waker::from(Arc::new(ThreadWaker(thread::current())));
    let mut cx = Context::from_waker(&waker);
    let start = std::time::Instant::now();
    loop {
        if future.as_mut().poll(&mut cx).is_ready() {
            return true;
        }
        thread::park_timeout(limit);
        if start.elapsed() >= limit {
            return false;
        }
    }
}

fn spin<F: Future>(future: F) {
    let mut future = pin!(future);
    let mut cx = Context::from_waker(Waker::noop());
    while future.as_mut().poll(&mut cx).is_pending() {}
}

fn main() {
    spin(Forgetful { asked: false });
    println!("spinning: finished");
    let limit = Duration::from_millis(100);
    let finished = finishes_in(Forgetful { asked: false }, limit);
    println!("sleeping: finished = {finished}");
}
```

```text
spinning: finished
sleeping: finished = false
```

Boşa dönen yöntemde hata görünmüyor, çünkü o zaten hep soruyor. Uyuyan çalıştırıcıda future bir daha yoklanmıyor. Burada süre sınırı koyduk; gerçek programda sessizce sonsuza kadar asılı kalırdı. Async kodda "program donuyor ama hata vermiyor" görünce ilk bakılacak yer burasıdır.

## Birçok iş: Görev ve kuyruk

Tek `block_on` tek future yürütür. Birçok işi yönetmek için iki kavram gerekir:

- **Görev** (task): Çalıştırıcının yönettiği üst düzey future.
- **Kuyruk**: Yoklanmaya hazır görevler.

Fikir tek cümle: Çalıştırıcı kuyruktan görev alır ve yoklar. `wake` ise görevi kuyruğa geri koyar. `Pending` dönen görev kuyrukta olmaz, yani **hiç işlemci harcamaz**.

```rust
use std::future::Future;
use std::pin::Pin;
use std::sync::mpsc::{Receiver, Sender, channel};
use std::sync::{Arc, Mutex};
use std::task::{Context, Poll, Wake, Waker};
use std::thread;
use std::time::{Duration, Instant};

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

async fn worker(name: &'static str, ms: u64) {
    Timer::new(ms).await;
    println!("{name} finished");
}

fn main() {
    let (sender, receiver) = channel();
    let start = Instant::now();
    spawn(&sender, worker("a", 150));
    spawn(&sender, worker("b", 50));
    spawn(&sender, worker("c", 100));
    drop(sender);
    run(receiver);
    println!("under 300 ms: {}", start.elapsed() < Duration::from_millis(300));
}
```

```text
b finished
c finished
a finished
under 300 ms: true
```

Parçaların görevi:

| Parça | Görevi |
|---|---|
| `Task` | Future ve kuyruğa geri dönüş yolu |
| `Mutex<Option<...>>` | Future'ı kullanmak için `&mut` gerekir; biten future `None` olur |
| `wake` | Görevi kuyruğa koyar |
| `spawn` | Görevi kurup kuyruğa ilk kez koyar |
| `run` | Kuyruktan al, yokla |
| `drop(sender)` | Görevler bitince kuyruk kapansın, `recv` hata versin, `run` bitsin |

Üç zamanlayıcının toplamı 300 milisaniye, ama iş bundan kısa sürdü, çünkü birlikte beklediler. Kısa olan önce bitti ve hepsi `run`'ın tek kolunda yazıldı.

## Send şartı

`spawn` future'ın `Send` olmasını istiyor, çünkü waker başka koldan çağrılabilir ve gerçek çalıştırıcılar görevleri kollar arasında gezdirir. Geçen bölümde `.await`'i aşan değişkenlerin future'ın içinde durduğunu görmüştük. Sonucu:

```rust
use std::future::Future;
use std::rc::Rc;

async fn pause() {}

async fn counted() {
    let count = Rc::new(1);
    pause().await;
    println!("{count}");
}

fn spawn<F: Future + Send>(_future: F) {}

fn main() {
    spawn(counted());
}
```

```text
error: future cannot be sent between threads safely
  --> main.rs:15:11
   |
15 |     spawn(counted());
   |           ^^^^^^^^^ future returned by `counted` is not `Send`
   |
   = help: within `impl Future<Output = ()>`, the trait `Send` is not implemented for
     `Rc<i32>`
note: future is not `Send` as this value is used across an await
  --> main.rs:8:13
   |
 7 |     let count = Rc::new(1);
   |         ----- has type `Rc<i32>` which is not `Send`
 8 |     pause().await;
   |             ^^^^^ await occurs here, with `count` maybe used later
note: required by a bound in `spawn`
  --> main.rs:12:22
   |
12 | fn spawn<F: Future + Send>(_future: F) {}
   |                      ^^^^ required by this bound in `spawn`
```

`Rc`, `.await`'i aştığı için future'ın parçası oldu ve future `Send` olmaktan çıktı. Çözüm: `Arc` kullanmak ya da `Rc`'yi `.await`'ten önce düşürmek.

## İptal: Düşürmek

Rust'ta future'ı durdurmanın ayrı bir yolu yoktur; **düşürmek** yeter. Düşen future bir daha yoklanmaz ve içindeki değerlerin `Drop`'u çalışır:

```rust
struct Noisy;

impl Drop for Noisy {
    fn drop(&mut self) {
        println!("cleanup");
    }
}

async fn job() {
    let _guard = Noisy;
    println!("started");
    std::future::pending::<()>().await;
    println!("never printed");
}

fn main() {
    let mut future = Box::pin(job());
    let mut cx = Context::from_waker(Waker::noop());
    let _ = future.as_mut().poll(&mut cx);
    drop(future);
    println!("dropped");
}
```

```text
started
cleanup
dropped
```

`job` `.await`'te bekliyordu; devamı hiç çalışmadı ama `_guard` temizlendi.

Bu fikir **select** kalıbının temelidir: İki future'ı birlikte yokla, ilk biteni al, ötekini düşür. "Şu iş 5 saniyede bitmezse vazgeç" böyle yazılır. Bedeli de vardır: Future `.await`'te her an iptal edilebilir, yani iki `.await` arasında yarım kalması sorun olan bir işi tek parça yapmak gerekir.

## Özet

- Uyuyan çalıştırıcı: `Pending` gelince `park`, waker gelince `unpark`.
- `Wake` trait'i `Arc`'lı türden `Waker` kurar.
- Future waker'ı her yoklamada saklar; işi yapan taraf bitince çağırır.
- Haber vermeyen future uyuyan çalıştırıcıda sessizce asılı kalır.
- Görev + kuyruk = çalıştırıcı. `wake` görevi kuyruğa koyar, bekleyen görev işlemci harcamaz.
- `spawn`'ın `Send` şartı yüzünden `.await`'i aşan `Rc` derlenmez.
- İptal etmek düşürmektir; `Drop` çalışır.

Sırada geçen iki bölümdür ertelediğimiz soru var: `Pin` neden var?
