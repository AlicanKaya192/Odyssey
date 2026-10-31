## Kim kimi uyandırır?

| Olay | Kim | Kimi |
|---|---|---|
| Zaman doldu | Zamanlayıcı kolu | `Sleep`'in görevi |
| Mesaj geldi | `send` | `recv` bekleyen görev |
| Son gönderici düştü | `Drop` | `recv` bekleyen görev |
| Görev bitti | `spawn` sarmalayıcısı | `JoinHandle` bekleyen görev |
| Waker çağrıldı | `Task::wake` | Görevi kuyruğa koyar |
| Kuyrukta görev var | `run` | Görevi yoklar |

## Bir mesajın yolculuğu

1. Alıcı `recv().await` der, kuyruk boş, waker saklanır, görev `Pending` döner ve kuyruktan çıkar.
2. Gönderen `send` çağırır, mesajı koyar, waker'ı alır.
3. Kilit bırakılır, `wake` çağrılır.
4. `Task::wake` görevi kuyruğa koyar.
5. `run` görevi alır ve yoklar; `recv` bu kez mesajı döndürür.

Arada alıcı görev hiç işlemci harcamaz.

## Türlerin taşıdığı sözler

| Tür | Söz | Nasıl |
|---|---|---|
| `Producer` | Tek üretici | Kopyalanamaz, `push(&mut self)` |
| `Consumer` | Tek tüketici | Kopyalanamaz, `pop(&mut self)` |
| `Recv` | Tek bekleyen alıcı | `recv(&mut self)` |
| `Spawner` | Görevler `Send` | `F: Send + 'static` |
| `Ring<T, N>` | `T` kol değiştirebilir | `T: Send` |

## Ring'in durumları

| Durum | Koşul |
|---|---|
| Boş | `head == tail` |
| Dolu | `tail - head == N` |
| Eleman sayısı | `tail - head` |
| Okunacak yuva | `head % N` |
| Yazılacak yuva | `tail % N` |

Sayaçlar hiç sıfırlanmaz ve kod düz çıkarma kullanır. 64 bitlik `usize`'ı doldurmaya bir ömür yetmez, bu yüzden taşma pratikte sorun değildir.

## Sıra kuralları

| İşlem | Sıralama | Neden |
|---|---|---|
| Kendi sayacını okumak | `Relaxed` | Yalnız sen yazıyorsun |
| Karşının sayacını okumak | `Acquire` | Yazılanı görmek için |
| Kendi sayacını yazmak | `Release` | Yazdığını göstermek için |
