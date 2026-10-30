## Yazımlar

| İş | Yazım |
|---|---|
| Ortak veri | `Arc::new(Mutex::new(v))` |
| Paylaş | `Arc::clone(&shared)` |
| Yaz | `*shared.lock().unwrap() += 1` |
| Çok okuyucu | `Arc::new(RwLock::new(v))` |
| Oku | `lock.read().unwrap()` |
| Yaz | `lock.write().unwrap()` |
| Atomik | `AtomicU32::new(0)` |
| Artır | `n.fetch_add(1, Ordering::SeqCst)` |
| Tek seferlik | `OnceLock` |

## Hangisi?

| İş | Seçim |
|---|---|
| Veri bir kola gidecek | `move` |
| Veriyi birkaç kol okuyacak, scope içinde | `&T` |
| Birkaç kol okuyacak, uzun yaşıyor | `Arc<T>` |
| Birkaç kol yazacak | `Arc<Mutex<T>>` |
| Çok okuma, az yazma | `Arc<RwLock<T>>` |
| Tek sayı | `AtomicU32` |
| Sonuçları topla | Kanal |

## Rc ile karşılığı

| Tek kol | Çok kol |
|---|---|
| `Rc<T>` | `Arc<T>` |
| `RefCell<T>` | `Mutex<T>`, `RwLock<T>` |
| `Cell<u32>` | `AtomicU32` |

## Kapsamlı kollarda Arc gerekmez

```rust
use std::sync::Mutex;
use std::thread;

fn main() {
    let total = Mutex::new(0);
    thread::scope(|s| {
        for n in 1..=3 {
            let total = &total;
            s.spawn(move || {
                *total.lock().unwrap() += n;
            });
        }
    });
    println!("{}", total.lock().unwrap());
}
```

```text
6
```

`thread::scope` ödünç izin verdiği için `Arc` gerekmez, `Mutex` yeter.
