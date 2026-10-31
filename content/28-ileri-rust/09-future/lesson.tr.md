# Future Elle Yazmak

Şimdiye kadar aynı anda birkaç iş yapmak için kol açtık. Ama bir sunucu on bin bağlantıyı bekliyorsa, işlerin çoğu yalnızca **bekliyordur**: Ağdan bir şey gelsin diye. Her bekleyişe bir kol ayırmak pahalıdır. Rust'ın cevabı `async`'tir ve onun altında tek bir trait vardır: `Future`.

Bu bölümde sihri kaldırıyoruz. `Future`'ı elle yazacak, elle yoklayacak, sonra `async fn`'in aslında ne ürettiğini göreceğiz.

## Future: Yoklanan iş

**Future**, henüz bitmemiş olabilecek bir iştir. Kendi kendine çalışmaz; biri ona "ilerleyebilir misin?" diye sorar. Bu soruya **poll** (yoklama) denir.

```rust
pub trait Future {
    type Output;

    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output>;
}

pub enum Poll<T> {
    Ready(T),
    Pending,
}
```

Üç parça var:

- `Output`: İş bitince verilecek değerin türü.
- `Poll<T>`: Yoklamanın cevabı. `Ready(değer)` bitti, `Pending` henüz değil.
- `poll`: Soruyu soran metot.

`Pin<&mut Self>` ilk başta korkutucu görünür. Şimdilik "taşınmayacağına söz verilmiş `&mut self`" diye oku; nedenini 11. bölümde göreceğiz. Bizim yazdığımız sade yapılarda `self.left` gibi alanlara doğrudan erişebiliriz.

`cx` (Context) içinde bir **waker** (uyandırıcı) taşır. Waker, "bu future yeniden yoklanmaya değer" diye haber vermenin yoludur.

## İlk future'ımız

İki kez "henüz değil" deyip sonra biten bir geri sayım:

```rust
use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Poll, Waker};

struct Countdown {
    left: u32,
}

impl Future for Countdown {
    type Output = &'static str;

    fn poll(mut self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output> {
        if self.left == 0 {
            return Poll::Ready("done");
        }
        self.left -= 1;
        cx.waker().wake_by_ref();
        Poll::Pending
    }
}

fn main() {
    let mut future = Countdown { left: 2 };
    let mut cx = Context::from_waker(Waker::noop());
    let mut pinned = Pin::new(&mut future);
    println!("{:?}", pinned.as_mut().poll(&mut cx));
    println!("{:?}", pinned.as_mut().poll(&mut cx));
    println!("{:?}", pinned.as_mut().poll(&mut cx));
}
```

```text
Pending
Pending
Ready("done")
```

Üç kez yokladık, üç cevap aldık. İşin ilerlemesi yalnızca biz sorunca oldu; arkada çalışan hiçbir şey yok.

`Waker::noop()` haber alınca hiçbir şey yapmayan hazır bir waker'dır. Elle denerken işimize yarar. `cx.waker().wake_by_ref()` ise "beni yine yokla" demektir. Burada kimse dinlemiyor, ama sözleşme bunu ister: `Pending` dönen future, yeniden yoklanacağından emin olmak zorundadır. Neden önemli olduğunu 10. bölümde ölçeceğiz.

## block_on: En küçük çalıştırıcı

Future'ları yoklayan program parçasına **çalıştırıcı** (executor) denir. Rust'ta dilin içinde çalıştırıcı yoktur, yazılır ya da crate olarak alınır. En küçüğü şudur: Bitene kadar yokla.

```rust
fn block_on<F: Future>(future: F) -> F::Output {
    let mut future = pin!(future);
    let mut cx = Context::from_waker(Waker::noop());
    loop {
        if let Poll::Ready(value) = future.as_mut().poll(&mut cx) {
            return value;
        }
    }
}

fn main() {
    println!("{}", block_on(Countdown { left: 3 }));
}
```

```text
done
```

`pin!` future'ı olduğu yerde sabitler ve yoklamak için gereken `Pin<&mut F>`'i verir. `F` herhangi bir future olabilir; sade bir yapı olmak zorunda değildir.

Bu `block_on` boşa döner: `Pending` alsa da hemen yeniden sorar. İşlemciyi boşuna yorar. Gerçek çalıştırıcı uyur ve waker'ı bekler; onu da 10. bölümde yazacağız.

## async fn: Future üreten fonksiyon

Elle `poll` yazmak yorucu. `async fn` aynı işi derleyiciye yaptırır. İlk şaşırtıcı nokta şu:

```rust
async fn greet(name: &str) -> String {
    println!("greet runs");
    format!("hello {name}")
}

fn main() {
    let future = greet("ada");
    println!("future created");
    let text = block_on(future);
    println!("{text}");
}
```

```text
future created
greet runs
hello ada
```

`greet("ada")` çağrısı gövdeyi **çalıştırmadı**. Yalnızca bir future döndürdü. Gövde ancak `block_on` yoklayınca çalıştı. Future'lar tembeldir.

## .await ne yapar?

`.await`, "bu iç future bitene kadar buradayım" der. Ama kolu durdurmaz. Her yoklamada ne olduğunu satır satır görelim:

```rust
struct Step {
    name: &'static str,
    left: u32,
}

impl Future for Step {
    type Output = ();

    fn poll(mut self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<()> {
        println!("  {} left {}", self.name, self.left);
        if self.left == 0 {
            return Poll::Ready(());
        }
        self.left -= 1;
        cx.waker().wake_by_ref();
        Poll::Pending
    }
}

async fn work() -> u32 {
    println!("start");
    Step { name: "a", left: 1 }.await;
    println!("a finished");
    Step { name: "b", left: 1 }.await;
    println!("b finished");
    7
}

fn main() {
    let mut future = pin!(work());
    let mut cx = Context::from_waker(Waker::noop());
    let mut round = 1;
    loop {
        println!("poll {round}");
        if let Poll::Ready(value) = future.as_mut().poll(&mut cx) {
            println!("result {value}");
            break;
        }
        round += 1;
    }
}
```

```text
poll 1
start
  a left 1
poll 2
  a left 0
a finished
  b left 1
poll 3
  b left 0
b finished
result 7
```

Çıktıyı dikkatle oku:

- `start` yalnızca bir kez yazıldı. İkinci yoklama baştan başlamadı, kaldığı yerden devam etti.
- `a` `Pending` deyince `work` da `Pending` döndü ve `main`'e çıktı. `.await` **beklemiyor, geri dönüyor**.
- `a` bitince `work` aynı yoklamanın içinde devam etti ve `b`'ye geldi.

Bir fonksiyon nasıl kaldığı yerden devam edebilir? Etmez. Derleyici onu başka bir şeye çevirir.

## async fn aslında durum makinesidir

`work`'ün yaptığını elle yazalım. "Neredeyim?" sorusunun cevabını bir `enum` tutar:

```rust
enum Work {
    Start,
    WaitA(Step),
    WaitB(Step),
    Done,
}

impl Future for Work {
    type Output = u32;

    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<u32> {
        let this = self.get_mut();
        loop {
            match this {
                Work::Start => {
                    println!("start");
                    *this = Work::WaitA(Step { name: "a", left: 1 });
                }
                Work::WaitA(step) => {
                    if Pin::new(step).poll(cx).is_pending() {
                        return Poll::Pending;
                    }
                    println!("a finished");
                    *this = Work::WaitB(Step { name: "b", left: 1 });
                }
                Work::WaitB(step) => {
                    if Pin::new(step).poll(cx).is_pending() {
                        return Poll::Pending;
                    }
                    println!("b finished");
                    *this = Work::Done;
                    return Poll::Ready(7);
                }
                Work::Done => panic!("polled after completion"),
            }
        }
    }
}

```

```text
poll 1
start
  a left 1
poll 2
  a left 0
a finished
  b left 1
poll 3
  b left 0
b finished
result 7
```

Çıktı `async fn` ile bire bir aynı. Derleyicinin ürettiği şey tam bu değildir ama fikir budur: Her `.await` bir durumdur, `poll` ise "bulunduğun durumdan devam et" demektir. Sihir yok; ürettiği, bizim de yazabileceğimiz bir `enum`.

Bu `enum` boyut hakkında da bir şey söyler: `.await`'i aşan her yerel değişken durumun içinde saklanmak zorundadır.

```rust
async fn pause() {}

async fn keeps_buffer() {
    let buffer = [1u8; 1024];
    pause().await;
    println!("{}", buffer[0]);
}

async fn drops_buffer() {
    {
        let buffer = [1u8; 1024];
        println!("{}", buffer[0]);
    }
    pause().await;
}

fn main() {
    println!("keeps: {}", size_of_val(&keeps_buffer()) > 1024);
    println!("drops: {}", size_of_val(&drops_buffer()) > 1024);
}
```

```text
keeps: true
drops: false
```

`keeps_buffer`'da dizi `.await`'ten sonra da lazım, bu yüzden future'ın içinde duruyor. `drops_buffer`'da kapsamı `.await`'ten önce bitiyor, future büyümüyor. Büyük değerleri `.await`'in öbür yanına taşımamak bu yüzden boş bir titizlik değildir.

## Tek kolda iki iş

Asıl kazanç burada. İki future'ı aynı anda ilerleten `Join` yazalım. `Yield` ise bir kez `Pending` deyip sırayı bırakan küçük bir future:

```rust
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

struct Join<A, B> {
    a: A,
    b: B,
    a_done: bool,
    b_done: bool,
}

impl<A, B> Future for Join<A, B>
where
    A: Future<Output = ()> + Unpin,
    B: Future<Output = ()> + Unpin,
{
    type Output = ();

    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<()> {
        let this = self.get_mut();
        if !this.a_done {
            this.a_done = Pin::new(&mut this.a).poll(cx).is_ready();
        }
        if !this.b_done {
            this.b_done = Pin::new(&mut this.b).poll(cx).is_ready();
        }
        if this.a_done && this.b_done {
            Poll::Ready(())
        } else {
            Poll::Pending
        }
    }
}

async fn worker(name: &str, rounds: u32) {
    for round in 0..rounds {
        println!("{name} {round}");
        Yield { done: false }.await;
    }
}

fn main() {
    let a = Box::pin(worker("a", 2));
    let b = Box::pin(worker("b", 2));
    block_on(Join { a, b, a_done: false, b_done: false });
}
```

```text
a 0
b 0
a 1
b 1
```

Tek kol var, ama işler dönüşümlü ilerledi. Buna **eşzamanlılık** (concurrency) denir; **paralellik** (parallelism) değildir, çünkü hiçbir an iki iş birden çalışmıyor.

`Box::pin`, `worker`'ın future'ını yığına (heap) koyup sabitler. Böylece `Join` onu rahatça `Pin::new` ile yoklayabilir. Sebebini de 11. bölümde göreceğiz.

Peki `Yield`'i kaldırırsak?

```rust
async fn worker(name: &str, rounds: u32) {
    for round in 0..rounds {
        println!("{name} {round}");
    }
}

```

```text
a 0
a 1
b 0
b 1
```

`a` hiç sıra bırakmadı. Burası `async`'in en önemli kuralı: Sıra yalnızca `.await`'te ve yalnızca iç future `Pending` derse el değiştirir. Çalıştırıcı kimseyi zorla durduramaz; işler **iş birliği** yapar. Bu yüzden `async` kodda uzun hesap ya da `thread::sleep` bütün kolu, yani öteki bütün future'ları durdurur.

## Neden bu kadar uğraş?

```rust
async fn worker(rounds: u32) -> u32 {
    for _ in 0..rounds {
        Yield { done: false }.await;
    }
    rounds
}

fn main() {
    let mut tasks: Vec<_> = (0..10_000).map(|_| Box::pin(worker(3))).collect();
    println!("one task under 1 KiB: {}", size_of_val(&*tasks[0]) < 1024);

    let mut cx = Context::from_waker(Waker::noop());
    let mut sum = 0;
    let mut rounds = 0;
    while !tasks.is_empty() {
        rounds += 1;
        tasks.retain_mut(|task| match task.as_mut().poll(&mut cx) {
            Poll::Ready(value) => {
                sum += value;
                false
            }
            Poll::Pending => true,
        });
    }
    println!("sum {sum}, rounds {rounds}");
}
```

```text
one task under 1 KiB: true
sum 30000, rounds 4
```

Tek kolda on bin iş dört turda bitti, her biri 1 KiB'den küçük. Rust'ta yeni bir kolun yığını ise belgeye göre şu an varsayılan 2 MiB. Bekleyen iş çoksa fark işte budur. İş bekleyen değil de hesap yapansa kazanç yoktur; orada kollar doğru cevaptır.

## Özet

- `Future`, `poll` ile yoklanan iştir: `Ready(değer)` ya da `Pending`.
- Future kendi kendine çalışmaz, onu çalıştırıcı yoklar.
- `async fn` çağırmak yalnızca future üretir; gövde ilk yoklamada çalışır.
- `.await` beklemez, `Pending`'i yukarı iletir; sonraki yoklamada kaldığı yerden devam edilir.
- `async fn` derleyicinin ürettiği bir durum makinesidir; `.await`'i aşan değişkenler onun içinde durur.
- Sıra yalnızca `.await`'te değişir. Eşzamanlılık var, paralellik yok.

Sırada gerçek bir çalıştırıcı var: Boşa dönmeyen, waker'la uyanan.
