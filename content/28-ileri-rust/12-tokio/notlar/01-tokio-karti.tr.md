## Birlikte yürütmek

| Yazım | Ne yapar |
|---|---|
| `tokio::spawn(fut)` | Yeni görev; `JoinHandle` verir |
| `handle.await` | Görevin sonucu: `Result<T, JoinError>` |
| `handle.abort()` | Görevi iptal eder |
| `tokio::join!(a, b)` | Aynı görevde birlikte, hepsini bekler |
| `tokio::try_join!(a, b)` | İlk `Err`'de durur |
| `tokio::select! { ... }` | İlk biteni çalıştırır, ötekileri düşürür |
| `spawn_blocking(f)` | Engelleyen işi ayrı havuza verir |
| `yield_now().await` | Sırayı başka göreve bırakır |

## Zaman

| Yazım | Ne yapar |
|---|---|
| `sleep(d).await` | İşçiyi kilitlemeden bekler |
| `timeout(d, fut).await` | `Result`: süre dolarsa `Err(Elapsed)` |
| `interval(d)` | Düzenli aralıkla `tick().await` |

```rust
use std::time::Duration;
use tokio::time::interval;

#[tokio::main]
async fn main() {
    let mut ticker = interval(Duration::from_millis(10));
    for n in 0..3 {
        ticker.tick().await;
        println!("tick {n}");
    }
}
```

```text
tick 0
tick 1
tick 2
```

İlk `tick` hemen döner.

## Kanal seçimi

| Kanal | Gönderici | Alıcı | Ne zaman |
|---|---|---|---|
| `mpsc` | Çok | Tek | İş kuyruğu |
| `oneshot` | Tek | Tek, tek mesaj | İsteğe cevap |
| `broadcast` | Çok | Çok, her biri her mesajı alır | Olay duyurusu |
| `watch` | Tek | Çok, yalnızca son değer | Ayar, durum |

```rust
use tokio::sync::{broadcast, watch};

#[tokio::main]
async fn main() {
    let (sender, mut first) = broadcast::channel(8);
    let mut second = sender.subscribe();
    sender.send("news").unwrap();
    println!("{} {}", first.recv().await.unwrap(), second.recv().await.unwrap());

    let (setter, reader) = watch::channel(1);
    setter.send(2).unwrap();
    setter.send(3).unwrap();
    println!("{}", *reader.borrow());
}
```

```text
news news
3
```

## Çalışma ortamı

| Yazım | Anlamı |
|---|---|
| `#[tokio::main]` | Çok iş parçacıklı ortam |
| `#[tokio::main(flavor = "current_thread")]` | Tek iş parçacığı |
| `Builder::new_multi_thread().enable_all().build()` | Elle kurmak |
| `runtime.block_on(fut)` | Normal koddan async koda geçiş |

`enable_all` zamanlayıcı ve ağ sürücülerini açar. Unutulursa `sleep` panikler.

## Feature'lar

Kendi projende `--features full` en rahatıdır. Derleme süresi önemliyse yalnızca gerekenler: `rt-multi-thread`, `macros`, `time`, `sync`, `net`, `io-util`.
