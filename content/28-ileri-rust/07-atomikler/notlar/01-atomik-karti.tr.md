## Türler

`AtomicBool`, `AtomicU8` … `AtomicU64`, `AtomicUsize`, `AtomicI32` …, `AtomicPtr<T>`. Hepsi `std::sync::atomic`'te. `static` olarak kullanılabilir, çünkü `new` `const`'tur ve işlemler `&self` alır.

## Yöntemler

| Çağrı | Döndürdüğü |
|---|---|
| `load(o)` | Değer |
| `store(v, o)` | Hiçbir şey |
| `swap(v, o)` | Eski değer |
| `fetch_add(v, o)`, `fetch_sub` | Eski değer |
| `fetch_or`, `fetch_and`, `fetch_xor` | Eski değer |
| `fetch_max`, `fetch_min` | Eski değer |
| `compare_exchange(e, y, b, h)` | `Ok(eski)` ya da `Err(gerçek)` |
| `compare_exchange_weak` | Aynı, boşuna düşebilir |
| `fetch_update(b, h, f)` | Kapanışlı döngü |

`fetch_add` taşınca sarar; panik yapmaz.

## compare_exchange kalıbı

```rust
let mut current = value.load(Ordering::Relaxed);
loop {
    let next = current * 2;
    match value.compare_exchange_weak(current, next, Ordering::AcqRel, Ordering::Relaxed) {
        Ok(_) => break,
        Err(actual) => current = actual,
    }
}
```

Döngü içindeyse `_weak` tercih edilir: Bazı işlemcilerde daha hızlıdır, boşuna düşse de döngü zaten yeniden dener. Döngü yoksa güçlü olan.

## Hangi sıralama nerede geçerli?

| İşlem | Geçerli |
|---|---|
| `load` | `Relaxed`, `Acquire`, `SeqCst` |
| `store` | `Relaxed`, `Release`, `SeqCst` |
| `fetch_*`, `swap` | Hepsi |
| `compare_exchange` başarı | Hepsi |
| `compare_exchange` hata | `Relaxed`, `Acquire`, `SeqCst` |

`load(Ordering::Release)` panik yapar: Okumanın "yayınlayacağı" bir şey yoktur.

## Ne zaman kilit?

| Durum | Seçim |
|---|---|
| Tek sayı ya da bayrak | Atomik |
| İki değer birlikte değişiyor | Kilit |
| Bir yapı (liste, harita) | Kilit |
| Kilit ölçülerek darboğaz çıktı | Düşün; önce parçalara böl |
