## Kilit iskeleti

| Parça | Yazım |
|---|---|
| Bayrak | `locked: AtomicBool` |
| Veri | `value: UnsafeCell<T>` |
| Söz | `unsafe impl<T: Send> Sync for Lock<T> {}` |
| Alma | `compare_exchange_weak(false, true, Acquire, Relaxed)` |
| Bırakma | `locked.store(false, Release)` |
| Kullanım | `Guard` + `Deref` + `DerefMut` + `Drop` |

## Bekleme bölümü

| Yazım | Anlamı |
|---|---|
| `std::hint::spin_loop()` | İşlemciye "döngüdeyim" |
| `thread::yield_now()` | Sırayı başka kola ver |
| `thread::park()` | Uyu, `unpark` bekler |

## Kilit aileleri

| Tür | Bekleyen ne yapar | Uygun iş |
|---|---|---|
| Spinlock | Döner | Çok kısa, çekirdeksiz |
| `Mutex` | Kısa döner, uyur | Genel |
| `RwLock` | Uyur | Çok okuma, az yazma |
| `Condvar` | Şart gerçekleşene kadar uyur | Üretici ve tüketici |
| `Barrier` | Herkes gelene kadar uyur | Toplu başlama |

## Kontrol listesi

| Soru | Yanlışsa |
|---|---|
| `Guard` `Send` değil mi? | Kilit başka kolda açılır |
| Panikte kilit açılıyor mu? | Herkes sonsuza kadar bekler |
| `T: Send` şartı var mı? | `Rc` kaçar |
| Kilit içinde başka kilit? | Ölü kilit sırası düşün |

Bizim `Guard`'ımız `&SpinLock<T>` tuttuğu için `T: Sync` ise `Send` olur; gerçek `MutexGuard` işletim sistemi kilidi yüzünden `Send` değildir. Spinlock'ta sakınca yoktur.
