# tokio

Son üç bölümde `Future`'ı, waker'ı, kendi çalıştırıcımızı ve `Pin`'i gördük. Rust dili yalnızca `Future`'ı tanımlar; onu
yürüten çalışma ortamı bir pakettir. Gerçek programların çoğunda bu paket **tokio**: İşçi iş parçacıkları, zamanlayıcı, ağ,
kanallar. Kendi çalıştırıcımızda elle yazdıklarımızın sağlam hâli.

Odyssey'de kaynağı programla geliyor. Kendi projende `cargo add tokio --features full` yazarsın. İlk derleme tokio'yu da
derlediği için uzun sürer (bu bilgisayarda yaklaşık 10 saniye), sonrası bir saniyenin altında.

## İlk program

```rust
#[tokio::main]
async fn main() {
    println!("hello from tokio");
}
```

```text
hello from tokio
```

`#[tokio::main]` bir attribute makrodur. `main` async olamaz, çünkü onu yürütecek kimse yoktur. Makro çalışma ortamını kurup
gövdeyi `block_on` ile çalıştırır, yani kabaca şunu yazar:

```rust
fn main() {
    let runtime = tokio::runtime::Builder::new_multi_thread()
        .enable_all()
        .build()
        .unwrap();
    runtime.block_on(async {
        println!("inside the runtime");
    });
}
```

```text
inside the runtime
```

`block_on`'u kendimiz yazmıştık. Buradaki farkı, altında birden çok işçi iş parçacığı olması ve boşta kalan işçinin
başkasının kuyruğundan iş çalması (work stealing).

## Ard arda değil, birlikte

`.await` kendiliğinden eşzamanlılık getirmez: Ard arda iki `.await`, biri bitince ötekini başlatır. Birlikte yürütmek için
`join!` yazılır:

```rust
use std::time::{Duration, Instant};
use tokio::time::sleep;

async fn work(name: &str) -> String {
    sleep(Duration::from_millis(200)).await;
    format!("{name} done")
}

#[tokio::main]
async fn main() {
    let start = Instant::now();
    let a = work("a").await;
    let b = work("b").await;
    println!("{a}, {b}");
    println!("at least 400 ms: {}", start.elapsed().as_millis() >= 400);

    let start = Instant::now();
    let (a, b) = tokio::join!(work("a"), work("b"));
    println!("{a}, {b}");
    println!("under 400 ms: {}", start.elapsed().as_millis() < 400);
}
```

```text
a done, b done
at least 400 ms: true
a done, b done
under 400 ms: true
```

Süre yerine karşılaştırma yazdırdık, çünkü süre her çalıştırmada değişir. `join!` iki future'ı **aynı görevde** sırayla
yoklar; biri beklerken öteki ilerler.

## Görev açmak: spawn

`tokio::spawn` yeni bir **görev** (task) açar. Görev, çalışma ortamının yürüttüğü bağımsız bir işlem birimidir, iş parçacığından
çok daha ucuzdur ve başka bir işçide çalışabilir. Bu yüzden future'ın `Send` ve `'static` olması gerekir; `async move`
gerekli veriyi içine alır.

```rust
use std::time::Duration;
use tokio::time::sleep;

#[tokio::main]
async fn main() {
    let mut handles = Vec::new();
    for id in 0..3u64 {
        handles.push(tokio::spawn(async move {
            sleep(Duration::from_millis(100 - id * 30)).await;
            println!("finished {id}");
            id * 10
        }));
    }
    for handle in handles {
        println!("result {}", handle.await.unwrap());
    }
}
```

```text
finished 2
finished 1
finished 0
result 0
result 10
result 20
```

Görevler 2, 1, 0 sırasıyla bitti, ama sonuçları bizim `await` sıramızla aldık. Görev açıldığı anda çalışmaya başlar;
`JoinHandle`'ı beklemek yalnızca sonucu almak içindir.

Görev panikleyince program durmaz, hata `JoinHandle`'dan döner:

```rust
#[tokio::main]
async fn main() {
    std::panic::set_hook(Box::new(|_| {}));
    let handle = tokio::spawn(async {
        let zero = "".len();
        10 / zero
    });
    let result = handle.await;
    println!("{}", result.is_err());
    println!("{}", result.unwrap_err().is_panic());
    println!("the program goes on");
}
```

```text
true
true
the program goes on
```

Buradaki `set_hook` yalnızca panik mesajını susturuyor, çıktı temiz kalsın diye.

## Yarış: select ve timeout

`select!` birkaç future'ı aynı anda bekler, **ilk biteni** çalıştırır ve ötekileri düşürür. `timeout` de aynı fikrin hazır
hâlidir:

```rust
use std::time::Duration;
use tokio::time::{sleep, timeout};

#[tokio::main]
async fn main() {
    tokio::select! {
        _ = sleep(Duration::from_millis(500)) => println!("slow won"),
        _ = sleep(Duration::from_millis(20)) => println!("fast won"),
    }

    let result = timeout(Duration::from_millis(20), sleep(Duration::from_secs(5))).await;
    println!("{result:?}");
    let result = timeout(Duration::from_millis(500), async { 42 }).await;
    println!("{result:?}");
}
```

```text
fast won
Err(Elapsed(()))
Ok(42)
```

**İptal** burada görünür hâle gelir. Rust'ta bir future'ı iptal etmek onu düşürmektir: Son `await` noktasından sonrası hiç
çalışmaz. Görevi dışarıdan durdurmak için `abort`:

```rust
use std::time::Duration;
use tokio::time::sleep;

#[tokio::main]
async fn main() {
    let handle = tokio::spawn(async {
        sleep(Duration::from_secs(60)).await;
        println!("never printed");
    });
    sleep(Duration::from_millis(10)).await;
    handle.abort();
    println!("{}", handle.await.unwrap_err().is_cancelled());
}
```

```text
true
```

## Kanallar

Görevler arasında veri paylaşmanın en temiz yolu mesaj göndermektir. `mpsc` çok göndericili, tek alıcılı kanaldır. `8`
kapasitedir: Kanal dolunca `send` bekler. Bu **geri basınç** (backpressure) hızlı üreticinin belleği doldurmasını engeller.

```rust
use tokio::sync::mpsc;

#[tokio::main]
async fn main() {
    let (sender, mut receiver) = mpsc::channel(8);
    for id in 0..3 {
        let sender = sender.clone();
        tokio::spawn(async move {
            sender.send(id * 10).await.unwrap();
        });
    }
    drop(sender);

    let mut got = Vec::new();
    while let Some(value) = receiver.recv().await {
        got.push(value);
    }
    got.sort();
    println!("{got:?}");
}
```

```text
[0, 10, 20]
```

`drop(sender)` önemli: `recv` bütün göndericiler düşene kadar `None` vermez. Kendi kopyamızı düşürmezsek döngü sonsuza kadar
bekler.

Bir görevin bir durumu yönetip isteklere cevap vermesi çok yaygın bir kalıptır. Cevap için `oneshot`, tek mesajlık kanal, isteğin
içine konur:

```rust
use tokio::sync::{mpsc, oneshot};

enum Request {
    Add(i32),
    Total(oneshot::Sender<i32>),
}

#[tokio::main]
async fn main() {
    let (sender, mut receiver) = mpsc::channel(8);
    tokio::spawn(async move {
        let mut total = 0;
        while let Some(request) = receiver.recv().await {
            match request {
                Request::Add(n) => total += n,
                Request::Total(reply) => reply.send(total).unwrap(),
            }
        }
    });

    sender.send(Request::Add(5)).await.unwrap();
    sender.send(Request::Add(7)).await.unwrap();
    let (reply, answer) = oneshot::channel();
    sender.send(Request::Total(reply)).await.unwrap();
    println!("{}", answer.await.unwrap());
}
```

```text
12
```

`total` tek bir görevin elinde olduğu için kilit gerekmiyor.

## Paylaşılan durum

Kısa bir iş için standart `Mutex` hâlâ doğru seçimdir ve daha hızlıdır:

```rust
use std::sync::{Arc, Mutex};

#[tokio::main]
async fn main() {
    let count = Arc::new(Mutex::new(0));
    let mut handles = Vec::new();
    for _ in 0..4 {
        let count = Arc::clone(&count);
        handles.push(tokio::spawn(async move {
            *count.lock().unwrap() += 1;
            tokio::task::yield_now().await;
        }));
    }
    for handle in handles {
        handle.await.unwrap();
    }
    println!("{}", count.lock().unwrap());
}
```

```text
4
```

Tek şart: Kilit `.await` boyunca tutulmaz. Tutarsan derleyici durdurur, çünkü `MutexGuard` başka iş parçacığına geçemez:

```rust
use std::sync::{Arc, Mutex};

#[tokio::main]
async fn main() {
    let count = Arc::new(Mutex::new(0));
    let handle = tokio::spawn(async move {
        let mut guard = count.lock().unwrap();
        tokio::task::yield_now().await;
        *guard += 1;
    });
    handle.await.unwrap();
}
```

```text
error: future cannot be sent between threads safely
   --> src/main.rs:6:18
    |
  6 |       let handle = tokio::spawn(async move {
    |  __________________^
  7 | |         let mut guard = count.lock().unwrap();
  8 | |         tokio::task::yield_now().await;
  9 | |         *guard += 1;
 10 | |     });
    | |______^ future created by async block is not `Send`
    |
    = help: within `{async block@src\main.rs:6:31: 6:41}`, the trait `Send` is not
      implemented for `std::sync::MutexGuard<'_, i32>`
note: future is not `Send` as this value is used across an await
   --> src/main.rs:8:34
    |
  7 |         let mut guard = count.lock().unwrap();
    |             --------- has type `std::sync::MutexGuard<'_, i32>` which is not
    `Send`
  8 |         tokio::task::yield_now().await;
    |                                  ^^^^^ await occurs here, with `mut guard` maybe
    used later
note: required by a bound in `tokio::spawn`
   --> rust-vendor/tokio/src/task/spawn.rs:176:21
    |
174 |     pub fn spawn<F>(future: F) -> JoinHandle<F::Output>
    |            ----- required by a bound in this function
175 |     where
176 |         F: Future + Send + 'static,
    |                     ^^^^ required by this bound in `spawn`
```

| İhtiyaç | Kullan |
|---|---|
| Kısa iş, await yok | `std::sync::Mutex` |
| Kilit await boyunca tutulacak | `tokio::sync::Mutex` |
| Durumu tek görev yönetsin | Kanal |

Aynı anda çalışan iş sayısını sınırlamak için `Semaphore`:

```rust
use std::sync::Arc;
use std::sync::atomic::{AtomicUsize, Ordering};
use std::time::Duration;
use tokio::sync::Semaphore;
use tokio::time::sleep;

#[tokio::main]
async fn main() {
    let permits = Arc::new(Semaphore::new(3));
    let running = Arc::new(AtomicUsize::new(0));
    let highest = Arc::new(AtomicUsize::new(0));
    let mut handles = Vec::new();
    for _ in 0..10 {
        let permits = permits.clone();
        let running = running.clone();
        let highest = highest.clone();
        handles.push(tokio::spawn(async move {
            let _permit = permits.acquire().await.unwrap();
            let now = running.fetch_add(1, Ordering::SeqCst) + 1;
            highest.fetch_max(now, Ordering::SeqCst);
            sleep(Duration::from_millis(20)).await;
            running.fetch_sub(1, Ordering::SeqCst);
        }));
    }
    for handle in handles {
        handle.await.unwrap();
    }
    println!("{}", highest.load(Ordering::SeqCst));
}
```

```text
3
```

On görev açtık, en fazla üçü aynı anda çalıştı. Dış servise aynı anda çok istek atmamak için kullanılır.

## İşçiyi kilitleme

Async'in en yaygın hatası: Görev **beklemek yerine engellerse** işçisi durur ve o işçideki başka görev çalışamaz. Farkı tek
iş parçacığında görelim:

```rust
use std::time::{Duration, Instant};

async fn blocks() {
    std::thread::sleep(Duration::from_millis(100));
}

async fn waits() {
    tokio::time::sleep(Duration::from_millis(100)).await;
}

#[tokio::main(flavor = "current_thread")]
async fn main() {
    let start = Instant::now();
    tokio::join!(blocks(), blocks(), blocks());
    println!("thread sleep, at least 300 ms: {}", start.elapsed().as_millis() >= 300);

    let start = Instant::now();
    tokio::join!(waits(), waits(), waits());
    println!("tokio sleep, under 300 ms: {}", start.elapsed().as_millis() < 300);
}
```

```text
thread sleep, at least 300 ms: true
tokio sleep, under 300 ms: true
```

Yoğun hesap ya da engelleyen bir kütüphane için ayrı bir iş parçacığı havuzu vardır:

```rust
fn heavy(n: u64) -> u64 {
    (1..=n).sum()
}

#[tokio::main]
async fn main() {
    let handle = tokio::task::spawn_blocking(|| heavy(1_000_000));
    println!("{}", handle.await.unwrap());
}
```

```text
500000500000
```

## Ağ

tokio'nun asıl çıkış sebebi budur. Binlerce bağlantı binlerce iş parçacığı istemez: Her bağlantı bir görevdir, veri gelene kadar
bekler. Burada yalnızca kendi bilgisayarında (`127.0.0.1`) çalışan bir sunucu ve istemci var; dışarı çıkılmıyor. Port `0`,
"boş bir port seç" demektir.

```rust
use tokio::io::{AsyncReadExt, AsyncWriteExt};
use tokio::net::{TcpListener, TcpStream};

#[tokio::main]
async fn main() -> std::io::Result<()> {
    let listener = TcpListener::bind("127.0.0.1:0").await?;
    let address = listener.local_addr()?;

    tokio::spawn(async move {
        loop {
            let (mut socket, _) = listener.accept().await.unwrap();
            tokio::spawn(async move {
                let mut buffer = [0; 64];
                let n = socket.read(&mut buffer).await.unwrap();
                socket.write_all(&buffer[..n]).await.unwrap();
            });
        }
    });

    for word in ["hello", "tokio"] {
        let mut client = TcpStream::connect(address).await?;
        client.write_all(word.as_bytes()).await?;
        let mut buffer = [0; 64];
        let n = client.read(&mut buffer).await?;
        println!("{}", String::from_utf8_lossy(&buffer[..n]));
    }
    Ok(())
}
```

```text
hello
tokio
```

`AsyncReadExt` ve `AsyncWriteExt`, `read` ve `write_all`'u getiren trait'lerdir. Sunucu her bağlantıya ayrı görev açıyor, böylece
yavaş bir istemci ötekileri bekletmiyor.

## Async test

`#[tokio::test]` her teste küçük bir çalışma ortamı kurar:

```rust
async fn double(n: i32) -> i32 {
    tokio::task::yield_now().await;
    n * 2
}

fn main() {}

#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn doubles() {
        assert_eq!(double(4).await, 8);
    }
}

```

```text
running 1 test
test tests::doubles ... ok
test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in
```

## Özet

- `#[tokio::main]` çalışma ortamı kurup async `main`'i `block_on` ile çalıştırır.
- Ard arda `.await` sıralıdır; `join!` aynı görevde birlikte yürütür, `spawn` yeni görev açar.
- `select!` ve `timeout` yarıştırır; iptal future'ı düşürmektir, await noktasında olur.
- `mpsc` çok göndericili, `oneshot` tek cevap; bütün göndericiler düşmeden `recv` `None` vermez.
- `std::sync::Mutex` kilit await boyunca tutulmuyorsa doğrudur; `Semaphore` eşzamanlılığı sınırlar.
- Async kodda engelleme: `spawn_blocking`.
