## Parçalar

| Ad | Ne işe yarar |
|---|---|
| `Future` | `poll` ile yoklanan iş |
| `Future::Output` | Bitince verilen değerin türü |
| `Poll::Ready(v)` | Bitti, değer `v` |
| `Poll::Pending` | Henüz değil |
| `Context` | Yoklamaya eşlik eder, waker'ı taşır |
| `cx.waker()` | O anki waker |
| `wake_by_ref()` | "Beni yine yokla" |
| `Waker::noop()` | Haber alınca hiçbir şey yapmayan waker |
| `pin!(f)` | Future'ı yerinde sabitler |
| `Box::pin(f)` | Future'ı yığında (heap) sabitler |

## Elle future kalıbı

| Adım | Kod |
|---|---|
| Bitti mi? | `return Poll::Ready(değer);` |
| Bitmedi | Durumu ilerlet |
| Haber ver | `cx.waker().wake_by_ref();` |
| Geri dön | `Poll::Pending` |

`Unpin` olan yapıda alanlara `self.alan` diye erişilir; alanın kendisini ödünç almak için `self.get_mut()` kullanılır. İç future'ı yoklamak için `Pin::new(&mut this.ic).poll(cx)`. Sade yapılar kendiliğinden `Unpin`'dir.

## async yazımları

| Yazım | Anlamı |
|---|---|
| `async fn f() -> T` | Çağrılınca `Output = T` olan future döndürür |
| `async { ... }` | Yerinde future üretir, çevreyi ödünç alır |
| `async move { ... }` | Çevreyi future'ın içine taşır |
| `f().await` | Bitene kadar devam etmez, bu arada `Pending` iletir |

## Standart kütüphanedeki hazırlar

| Ad | Davranış |
|---|---|
| `std::future::ready(v)` | İlk yoklamada `Ready(v)` |
| `std::future::pending()` | Hiç bitmez |
| `std::future::poll_fn(f)` | Kapanıştan future yapar |

## Kol mu, async mi?

| İş | Doğru araç |
|---|---|
| Çoğunlukla bekliyor (ağ, disk) | `async` |
| Çoğunlukla hesap yapıyor | Kol |
| Az sayıda bekleyen iş | Kol daha basit |
| On binlerce bağlantı | `async` |
