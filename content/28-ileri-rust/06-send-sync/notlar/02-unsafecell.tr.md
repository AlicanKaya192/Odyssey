## UnsafeCell kuralları

`UnsafeCell<T>::get(&self)` `*mut T` verir. Derleyiciye "buradaki değer `&` üzerinden değişebilir" der; iyileştirmeleri buna göre yapar. Yine de iki kural senindir:

| Kural | Bozulursa |
|---|---|
| Aynı anda hem `&mut T` hem başka referans olamaz | Tanımsız davranış |
| Kollar arası erişim eşzamanlı olmalı | Veri yarışı |

## Hangi tür neyi ekler?

| Tür | `UnsafeCell` üstüne | Denetim |
|---|---|---|
| `Cell<T>` | Referans vermeme | Referans yok, güvenli |
| `RefCell<T>` | Ödünç sayacı | Çalışma anında, panik |
| `Mutex<T>` | İşletim sistemi kilidi | Kollar arası, bekler |
| `AtomicU32` | Atomik işlem | Kollar arası, kilitsiz |
| `OnceLock<T>` | Bir kez yazma | Kollar arası |

## Yasak kestirme

`&T`'yi `*mut T`'ye çevirip yazmak, `UnsafeCell` olmadan **her zaman** tanımsız davranıştır:

```rust
let x = 1;
let r = &x;
let p = r as *const i32 as *mut i32;
// unsafe { *p = 2 };  // undefined behavior, even if it appears to work
```

Derleyici `x`'in değişmediğini varsayar ve okumayı sabit `1` ile değiştirebilir. Yazmanın etkisi hiç görünmeyebilir. Bu yüzden `Cell` gibi bir tür gerekir; basit bir "iyileştirme kapatma" değildir.
