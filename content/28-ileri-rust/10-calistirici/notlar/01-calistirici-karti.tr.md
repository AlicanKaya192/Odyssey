## Uyuyan block_on

| Adım | Kod |
|---|---|
| Waker kur | `Waker::from(Arc::new(ThreadWaker(thread::current())))` |
| Context kur | `Context::from_waker(&waker)` |
| Sabitle | `pin!(future)` |
| Yokla | `future.as_mut().poll(&mut cx)` |
| `Pending` | `thread::park()` |
| `Ready(v)` | `return v` |

## Waker kuralları

| Kural | Neden |
|---|---|
| `Pending` dönen future haber vermeyi garantiler | Yoksa asılı kalır |
| Son yoklamanın waker'ı geçerlidir | Future başka göreve geçebilir |
| Durum kontrolü ve saklama aynı kilit altında | Yoksa haber kaybolur |
| `wake` kilit bırakıldıktan sonra | Uyanan iş kilidi beklemesin |
| `wake` birden çok kez çağrılabilir | Fazladan yoklama zararsızdır |
| `wake` hemen dönmelidir | Çağıran kolu bekletmesin |

## wake ve wake_by_ref

| Metot | Fark |
|---|---|
| `waker.wake()` | Waker'ı tüketir; saklanan waker bir daha lazım değilse |
| `waker.wake_by_ref()` | Ödünç alır |
| `waker.clone()` | Saklamak için kopya |

## Küçük çalıştırıcı

| Parça | Kod |
|---|---|
| Kuyruk | `channel()` |
| Görev | `Task { future: Mutex<Option<BoxFuture>>, queue: Sender<Arc<Task>> }` |
| Uyandırma | `queue.send(self)` |
| Döngü | `while let Ok(task) = queue.recv()` |
| Bitiş | Bütün `Sender`'lar düşünce |

`BoxFuture` = `Pin<Box<dyn Future<Output = ()> + Send>>`. Farklı `async fn`'lerin türleri farklıdır; aynı kuyrukta durabilmeleri için `dyn` gerekir.

## Eşzamanlılık kalıpları

| Kalıp | Ne yapar | Biten olunca |
|---|---|---|
| join | İkisini de bekler | İkisi de bitince sonuç |
| select | İlk biteni alır | Öteki düşürülür |
| spawn | Bağımsız görev | Çalıştırıcı yürütür |
