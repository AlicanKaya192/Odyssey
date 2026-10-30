# Atomikler ve Bellek Sıralaması

Atomik işlem, başka kolun ortasını göremediği işlemdir. Temel türler için kilitsiz paylaşım sağlar. Modülün en zor bölümü burada: İşlemlerin hangi sırayla göründüğü.

## Neden gerekli?

`x += 1` tek bir işlem değildir: Oku, ekle, yaz. İki kol aynı anda yaparsa biri ötekinin artışını ezer. `fetch_add` bunu tek adımda yapar:

```rust
use std::sync::atomic::{AtomicU32, Ordering};
use std::thread;

static HITS: AtomicU32 = AtomicU32::new(0);

fn main() {
    thread::scope(|s| {
        for _ in 0..4 {
            s.spawn(|| {
                for _ in 0..1000 {
                    HITS.fetch_add(1, Ordering::SeqCst);
                }
            });
        }
    });
    println!("{}", HITS.load(Ordering::SeqCst));
}
```

```text
4000
```

Sonuç her çalıştırmada aynıdır. `Mutex` olmadan, çünkü tek sayı için kilit fazla.

## İşlemler

| Çağrı | İş |
|---|---|
| `load(o)` | Oku |
| `store(v, o)` | Yaz |
| `fetch_add(v, o)` | Ekle, **eskiyi** döndür |
| `swap(v, o)` | Yaz, eskiyi döndür |
| `compare_exchange(eski, yeni, b, h)` | Eskiyse yaz |
| `fetch_update(...)` | Kapanışla döngülü değiştir |

`compare_exchange` kilitsiz yapıların temelidir. "Değer hâlâ beklediğim gibiyse değiştir" der ve sonucu `Result` ile bildirir:

```rust
use std::sync::atomic::{AtomicU32, Ordering};

fn main() {
    let value = AtomicU32::new(5);
    println!("{:?}", value.compare_exchange(5, 6, Ordering::SeqCst, Ordering::SeqCst));
    println!("{:?}", value.compare_exchange(5, 7, Ordering::SeqCst, Ordering::SeqCst));
    println!("{}", value.load(Ordering::SeqCst));
}
```

```text
Ok(5)
Err(6)
6
```

Böylece her artış işleminin yapamadığı şeyler yazılabilir. En büyük değeri tutan sayaç gibi:

```rust
use std::sync::atomic::{AtomicU32, Ordering};
use std::thread;

fn store_max(slot: &AtomicU32, value: u32) {
    let mut current = slot.load(Ordering::SeqCst);
    while value > current {
        match slot.compare_exchange(current, value, Ordering::SeqCst, Ordering::SeqCst) {
            Ok(_) => return,
            Err(actual) => current = actual,
        }
    }
}

fn main() {
    let best = AtomicU32::new(0);
    thread::scope(|s| {
        for n in [3, 9, 4, 7] {
            let best = &best;
            s.spawn(move || store_max(best, n));
        }
    });
    println!("{}", best.load(Ordering::SeqCst));
}
```

```text
9
```

Döngü şart: Biz okuduktan sonra başka kol değiştirmişse `compare_exchange` düşer, yeni değerle yeniden deneriz.

## Bellek sıralaması

Her atomik işlem bir `Ordering` alır. İşlemci ve derleyici, tek kolda sonucu değiştirmeyen okuma ve yazmaları yeniden sıralayabilir. `Ordering` bunun ne kadarına izin verdiğini söyler:

| Sıralama | Sözü | Kullanım |
|---|---|---|
| `Relaxed` | Yalnızca o işlem atomik | Bağımsız sayaç |
| `Release` | Önceki yazmalar öne geçmez | Veriyi yayınlamak |
| `Acquire` | Sonraki okumalar öne geçmez | Yayınlananı almak |
| `AcqRel` | İkisi birden | `fetch_add` gibi oku-yaz |
| `SeqCst` | Bütün kollar aynı sırayı görür | Emin değilsen |

## Yayınlamak: Release ve Acquire

En önemli kalıp şudur. Bir kol veriyi hazırlar, sonra bayrağı `Release` ile yazar. Öbür kol bayrağı `Acquire` ile okuyup `true` görürse verinin hazır olduğundan emindir:

```rust
use std::sync::atomic::{AtomicBool, AtomicU32, Ordering};
use std::thread;

static DATA: AtomicU32 = AtomicU32::new(0);
static READY: AtomicBool = AtomicBool::new(false);

fn main() {
    thread::scope(|s| {
        s.spawn(|| {
            DATA.store(42, Ordering::Relaxed);
            READY.store(true, Ordering::Release);
        });
        s.spawn(|| {
            while !READY.load(Ordering::Acquire) {
                std::hint::spin_loop();
            }
            println!("{}", DATA.load(Ordering::Relaxed));
        });
    });
}
```

```text
42
```

`Relaxed` yazsaydık `DATA` için söz kalmazdı: Kol bayrağı görüp veriyi eski değerinde okuyabilirdi. Bu hata çoğu makinede görünmez, başka mimaride görünür. Tam bu yüzden sıralama **gerekçeyle** seçilir, denenerek değil.

## Sayaçta Relaxed yeterli

Sayaç başka veriyi korumuyorsa sıralama gerekmez. Sonuç yine doğrudur, çünkü `fetch_add` atomiktir:

```rust
use std::sync::atomic::{AtomicU64, Ordering};
use std::thread;

fn main() {
    let total = AtomicU64::new(0);
    thread::scope(|s| {
        for _ in 0..8 {
            s.spawn(|| {
                for _ in 0..10_000 {
                    total.fetch_add(1, Ordering::Relaxed);
                }
            });
        }
    });
    println!("{}", total.load(Ordering::Relaxed));
}
```

```text
80000
```

## Neyi seçmeli?

| Durum | Seçim |
|---|---|
| Bağımsız sayaç, istatistik | `Relaxed` |
| "Bu veri hazır" bayrağı | `Release` / `Acquire` |
| Kilit | `Acquire` / `Release` |
| Emin değilim | `SeqCst` |

`SeqCst` her zaman doğrudur ama "kilitlerden hızlıdır" demek değildir. Çoğu programda fark ölçülemez; önce doğru olsun.

## Önbellek satırı

Atomikler ucuz görünür ama iki kol aynı önbellek satırına yazarsa işlemciler satırı birbirinden kapar. Değişkenler farklı olsa bile. Buna **yanlış paylaşım** (false sharing) denir, `#[repr(align(64))]` değişkenleri ayırır:

```rust
use std::sync::atomic::AtomicU64;

struct Together {
    a: AtomicU64,
    b: AtomicU64,
}

#[repr(align(64))]
struct OnItsOwnLine(AtomicU64);

struct Apart {
    a: OnItsOwnLine,
    b: OnItsOwnLine,
}

fn main() {
    println!("{}", size_of::<Together>());
    println!("{}", size_of::<Apart>());
}
```

```text
16
128
```

## Özet

- Atomik işlem bölünmez: `fetch_add`, `compare_exchange`.
- `compare_exchange` döngüsü, kilitsiz yapının temelidir.
- `Relaxed`: Yalnızca o değer. `Release`/`Acquire`: Veri yayınlamak.
- `SeqCst` emin olmadığında, ama hızdan önce doğruluk.
- Sıralama hatası testte görünmeyebilir; gerekçeyle seç.
