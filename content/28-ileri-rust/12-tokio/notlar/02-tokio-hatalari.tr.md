## Belirti ve sebep

| Belirti | Sebep | Çözüm |
|---|---|---|
| `futures do nothing unless you .await or poll them` | `.await` unutuldu, gövde hiç çalışmadı | `work().await` |
| `future cannot be sent between threads safely` | Await boyunca `Rc` ya da `MutexGuard` tutuldu | Kilidi await'ten önce bırak, `Arc` kullan |
| `` `x` does not live long enough`` | `spawn`'a ödünç verildi | `async move`, `Arc` |
| Program bitmiyor | Kanalın göndericisi yaşıyor | `drop(sender)` |
| Görevler sırayla çalışıyor | Async kodda engelleyen çağrı | `spawn_blocking`, `tokio::time::sleep` |
| Sonuç yazılmadan program bitti | `spawn` edilen görev beklenmedi | `handle.await` |

## Görev beklenmezse

`main` bitince çalışma ortamı kapanır ve bitmemiş görevler düşürülür. Sonucunu istediğin görevi beklersin.

## Kanalı boş bekleyen alıcı

Kanal boşken `recv` `None` değil, bekleme demektir. `None` yalnızca bütün göndericiler düşünce gelir:

```rust
use std::time::Duration;
use tokio::sync::mpsc;
use tokio::time::timeout;

#[tokio::main]
async fn main() {
    let (sender, mut receiver) = mpsc::channel(8);
    sender.send(1).await.unwrap();
    println!("{:?}", receiver.recv().await);
    let waited = timeout(Duration::from_millis(50), receiver.recv()).await;
    println!("{}", waited.is_err());
    drop(sender);
    println!("{:?}", receiver.recv().await);
}
```

```text
Some(1)
true
None
```

İkinci satır bekledi ve zaman aşımına uğradı, çünkü `sender` hâlâ yaşıyordu. `drop` sonrası hemen `None` geldi.

## İptal güvenli mi?

`select!` kaybeden dalı düşürür. Dal bir işin ortasındaysa iş yarım kalır. Bir `await` noktasında kesilmenin zararı yoksa buna **iptal güvenli** (cancel safe) denir.

| Çağrı | İptal güvenli mi |
|---|---|
| `mpsc::Receiver::recv` | Evet, mesaj kaybolmaz |
| `sleep` | Evet |
| `AsyncReadExt::read` | Evet |
| `AsyncWriteExt::write_all` | Hayır, bir kısmı yazılmış olabilir |

Tokio'nun belgesi her metot için bunu söyler.
