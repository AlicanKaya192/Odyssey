## Tuzaklar

| Tuzak | Açıklama |
|---|---|
| Okuyup sonra yazmak | `load` sonra `store` iki işlemdir, araya kol girer |
| Bayrakta `Relaxed` | Veri için söz yok |
| Ayrı atomiklerde tutarlılık | İki atomik birlikte değişmez, kilit gerek |
| Yalnızca testle doğrulamak | x86 sıralamayı daha sıkı verir; hata başka işlemcide çıkar |
| `fetch_add` sonrası `load` | Sonucu değil, başka kolun değerini okuyabilir: `fetch_add`'in dönüşünü kullan |

## İlk tuzak

```rust
// WRONG: another branch can step in between.
let value = counter.load(Ordering::SeqCst);
counter.store(value + 1, Ordering::SeqCst);
```

Hiçbir `Ordering` bunu düzeltmez. Sıralama yalnızca görünme sırasını belirler, iki işlemi tek işlem yapmaz.

## x86 ve ARM

| İşlemci | Davranış |
|---|---|
| x86 | Yazmalar sırayla görünür; `Release`/`Acquire` çoğunlukla bedava |
| ARM, RISC-V | Yeniden sıralar; `Relaxed` hatası gerçekten çıkar |

Bu yüzden x86'da "çalışıyor" demek hiçbir şey göstermez. Program bir gün telefonda ya da yeni nesil dizüstünde koşabilir.

## Hazırı kullan

| İhtiyaç | Hazır tür |
|---|---|
| Bir kez başlatma | `OnceLock<T>`, `LazyLock<T>` |
| Sayaçlı paylaşım | `Arc<T>` |
| Kilit | `Mutex`, `RwLock` |
| Kanal | `mpsc` |
| Kolları bekletmek | `Barrier`, `Condvar` |

Kendi atomik algoritmanı yazmak son çaredir. Standart türler uzman gözünden geçti.
