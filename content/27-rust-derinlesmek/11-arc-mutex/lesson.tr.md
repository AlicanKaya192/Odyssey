# Arc ve Mutex

Kanal veriyi taşır. Bazen ise birçok kolun **aynı veriye** erişmesi gerekir: Ortak sayaç, ortak önbellek. Bunun için iki parça: Birden çok sahip için `Arc`, aynı anda tek erişim için `Mutex`.

## Mutex: Tek seferde bir kol

`Mutex` (mutual exclusion, karşılıklı dışlama) içindeki veriyi kilitle korur. Veriye ulaşmanın **tek yolu** kilidi almaktır, yani kilidi unutmak derlenmez:

```rust
use std::sync::Mutex;

fn main() {
    let value = Mutex::new(5);
    {
        let mut guard = value.lock().unwrap();
        *guard += 1;
    }
    println!("{:?}", value.lock().unwrap());
}
```

```text
6
```

| Parça | Anlamı |
|---|---|
| `Mutex::new(5)` | Korunan değer |
| `.lock()` | Kilidi bekler, `Result` döndürür |
| `unwrap` | Kilit zehirlenmediyse (aşağıda) |
| Koruyucu | `*guard` ile değere erişilir |

**Kilit kapsam sonunda kendiliğinden açılır**: `MutexGuard`'ın `Drop`'u. RAII burada güvenlik sağlıyor: Kilidi bırakmayı unutamazsın.

## Sorun: Birden çok kol

```rust
use std::sync::Mutex;
use std::thread;

fn main() {
    let counter = Mutex::new(0);
    let a = thread::spawn(move || *counter.lock().unwrap() += 1);
    let b = thread::spawn(move || *counter.lock().unwrap() += 1);
    a.join().unwrap();
    b.join().unwrap();
}
```

```text
error[E0382]: use of moved value: `counter`
 --> main.rs:7:27
  |
5 |     let counter = Mutex::new(0);
  |         ------- move occurs because `counter` has type `std::sync::Mutex<i32>`,
  which does not implement the `Copy` trait
6 |     let a = thread::spawn(move || *counter.lock().unwrap() += 1);
  |                           -------  ------- variable moved due to use in closure
  |                           |
  |                           value moved into closure here
7 |     let b = thread::spawn(move || *counter.lock().unwrap() += 1);
  |                           ^^^^^^^  ------- use occurs due to use in closure
  |                           |
  |                           value used here after move
```

Sahiplik ilk kola gitti, ikincisi alamıyor. Birden çok sahip gerekiyor. `Rc` denersek `Send` değil. Çözüm `Arc`.

## Arc: Atomik sayaç

`Arc<T>` (atomic reference counted), `Rc` ile aynıdır, ama sayacı işlemcinin atomik işlemleriyle güncellediği için iş parçacıkları arasında güvenlidir. Bedeli biraz yavaşlıktır, bu yüzden `Rc` hâlâ vardır.

```rust
use std::sync::{Arc, Mutex};
use std::thread;

fn main() {
    let counter = Arc::new(Mutex::new(0));
    let mut handles = Vec::new();
    for _ in 0..4 {
        let counter = Arc::clone(&counter);
        handles.push(thread::spawn(move || {
            for _ in 0..1000 {
                *counter.lock().unwrap() += 1;
            }
        }));
    }
    for h in handles {
        h.join().unwrap();
    }
    println!("{}", counter.lock().unwrap());
}
```

```text
4000
```

Her zaman aynı sonuç: 4 kol, her biri 1000 kez artırdı. Kilit olmasaydı derlenmezdi.

<figure class="fig"><svg viewBox="0 0 640 226" width="640" xmlns="http://www.w3.org/2000/svg"><text class="dim" x="20" y="24" font-size="13" font-weight="600">yığın (stack)</text><text class="dim" x="390" y="24" font-size="13" font-weight="600">öbek (heap)</text><g><rect class="box" x="20" y="44" width="230" height="44" rx="8"/><text class="ink" x="34" y="71" font-size="14" font-weight="600">counter</text><text class="dim" x="110" y="71" font-size="12.5">Arc</text></g><g><rect class="box" x="20" y="102" width="230" height="44" rx="8"/><text class="ink" x="34" y="129" font-size="14" font-weight="600">1. kol / branch 1</text><text class="dim" x="110" y="129" font-size="12.5">Arc</text></g><g><rect class="box" x="20" y="160" width="230" height="44" rx="8"/><text class="ink" x="34" y="187" font-size="14" font-weight="600">2. kol / branch 2</text><text class="dim" x="110" y="187" font-size="12.5">Arc</text></g><g><rect class="box" x="390" y="44" width="220" height="44" rx="8"/><text class="ink" x="404" y="71" font-size="14">sayaç 3, Mutex(0)</text></g><path class="curve" d="M250 66 C320 66 320 66 382 66"/><polygon class="dot" points="390,66 380,61 380,71"/><path class="curve" d="M250 124 C320 124 320 66 382 66"/><polygon class="dot" points="390,66 380,61 380,71"/><path class="curve" d="M250 182 C320 182 320 66 382 66"/><polygon class="dot" points="390,66 380,61 380,71"/></svg><figcaption>Her kolun kendi Arc'ı var, hepsi aynı Mutex'i gösteriyor.</figcaption></figure>

## Hesabı dışarıda yap

Kilit tutulurken ötekiler bekler. Bu yüzden kilidi **olabildiğince kısa** tut:

```rust
use std::sync::Mutex;

fn expensive(n: u64) -> u64 {
    (1..=n).sum()
}

fn main() {
    let results = Mutex::new(Vec::new());
    let value = expensive(1000);
    {
        let mut list = results.lock().unwrap();
        list.push(value);
    }
    println!("{:?}", results.lock().unwrap());
}
```

```text
[500500]
```

Pahalı hesabı kilitten önce yap, yalnızca sonucu yazarken kilitle. Blok içine almak koruyucuyu erken bırakır.

## RwLock: Çok okuyucu

Çoğunlukla okunuyorsa `RwLock` birçok okuyucuya aynı anda izin verir, yazıcı tek başına kalır:

```rust
use std::sync::RwLock;

fn main() {
    let config = RwLock::new(String::from("v1"));
    {
        let a = config.read().unwrap();
        let b = config.read().unwrap();
        println!("{a} {b}");
    }
    config.write().unwrap().push_str("-new");
    println!("{}", config.read().unwrap());
}
```

```text
v1 v1
v1-new
```

Ödünç alma kuralının çalışma anındaki karşılığı. Yazma çoksa `Mutex` daha hızlı olabilir.

## Atomikler

Tek bir sayı için kilit gerekmez:

```rust
use std::sync::atomic::{AtomicU32, Ordering};
use std::thread;

fn main() {
    let hits = AtomicU32::new(0);
    thread::scope(|s| {
        for _ in 0..4 {
            s.spawn(|| {
                for _ in 0..1000 {
                    hits.fetch_add(1, Ordering::SeqCst);
                }
            });
        }
    });
    println!("{}", hits.load(Ordering::SeqCst));
}
```

```text
4000
```

`Ordering::SeqCst` en güçlü ve en anlaşılır seçenektir. Diğerlerini İleri modülde göreceğiz. Şimdilik kural: Emin değilsen `SeqCst`.

## Zehirlenme

Kilit tutan kol panik yaparsa `Mutex` **zehirlenir** (poisoned): Veri yarım kalmış olabilir, bu yüzden sonraki `lock()` `Err` verir:

```rust
use std::sync::{Arc, Mutex};
use std::thread;

fn main() {
    let shared = Arc::new(Mutex::new(1));
    let copy = Arc::clone(&shared);
    let _ = thread::spawn(move || {
        let _guard = copy.lock().unwrap();
        panic!("oops");
    })
    .join();
    println!("{}", shared.is_poisoned());
    println!("{}", shared.lock().is_err());
}
```

```text
true
true
```

`unwrap` çoğu zaman doğru seçimdir: Panik yayılsın. Veriyi yine de kullanmak istersen `into_inner` ile alırsın.

## Ölü kilit

İki kol iki kilidi ters sırayla alırsa ikisi de sonsuza kadar bekler. Buna **ölü kilit** (deadlock) denir. **Rust bunu engellemez.** Veri yarışı derlenmez, ölü kilit derlenir.

| Önlem | |
|---|---|
| Kilitleri her yerde aynı sırayla al | En güvenlisi |
| Kilit tutarken başka kilit alma | Mümkünse |
| Kilidi kısa tut | Her zaman |

Aynı kol aynı `Mutex`'i iki kez kilitlerse de takılır ya da panikler.

## Özet

- `Mutex<T>`: Veriye yalnızca kilitle ulaşılır; `MutexGuard` düşünce kilit açılır.
- `Arc<T>`: Kollar arası çok sahip. `Arc<Mutex<T>>` standart ikilidir.
- Kilidi kısa tut; hesabı dışarıda yap.
- `RwLock` çok okuyucu; `AtomicU32` gibi türler tek sayı için.
- Panik kilidi zehirler. Ölü kilidi Rust engellemez: Sırayı sen koru.
