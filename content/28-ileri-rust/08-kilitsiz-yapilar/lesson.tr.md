# Spinlock ve Kilitsiz Yapılar

Atomikleri ve `UnsafeCell`'i öğrendik. İkisini birleştirince kendi kilidimizi yazabiliriz. Bu bölümde önce bir **spinlock**, sonra kilitsiz bir yığın kuruyoruz.

## Parçalar

Kilit için iki şey gerekir: "Dolu mu?" bayrağı ve korunan veri.

```rust
use std::cell::UnsafeCell;
use std::sync::atomic::AtomicBool;
use std::thread;

struct SpinLock<T> {
    locked: AtomicBool,
    value: UnsafeCell<T>,
}

fn main() {
    let lock = SpinLock { locked: AtomicBool::new(false), value: UnsafeCell::new(0) };
    thread::scope(|s| {
        s.spawn(|| &lock);
    });
}
```

```text
error[E0277]: `UnsafeCell<{integer}>` cannot be shared between threads safely
  --> main.rs:13:11
   |
13 |         s.spawn(|| &lock);
   |           ^^^^^ `UnsafeCell<{integer}>` cannot be shared between threads safely
   |
   = help: within `SpinLock<{integer}>`, the trait `Sync` is not implemented for
     `UnsafeCell<{integer}>`
note: required because it appears within the type `SpinLock<{integer}>`
  --> main.rs:5:8
   |
 5 | struct SpinLock<T> {
   |        ^^^^^^^^
   = note: required for `&SpinLock<{integer}>` to implement `Send`
note: required by a bound in `Scope::<'scope, 'env>::spawn`
```

Derleyici haklı: `UnsafeCell` `Sync` değildir. Söz verecek olan biziz, çünkü bayrak erişimi sıraya sokacak.

## Spinlock

```rust
use std::cell::UnsafeCell;
use std::ops::{Deref, DerefMut};
use std::sync::atomic::{AtomicBool, Ordering};
use std::thread;

pub struct SpinLock<T> {
    locked: AtomicBool,
    value: UnsafeCell<T>,
}

// SAFETY: the flag gives one access at a time, so T only needs to be Send.
unsafe impl<T: Send> Sync for SpinLock<T> {}

impl<T> SpinLock<T> {
    pub fn new(value: T) -> Self {
        SpinLock { locked: AtomicBool::new(false), value: UnsafeCell::new(value) }
    }

    pub fn lock(&self) -> Guard<'_, T> {
        while self
            .locked
            .compare_exchange_weak(false, true, Ordering::Acquire, Ordering::Relaxed)
            .is_err()
        {
            std::hint::spin_loop();
        }
        Guard { lock: self }
    }
}

pub struct Guard<'a, T> {
    lock: &'a SpinLock<T>,
}

impl<T> Deref for Guard<'_, T> {
    type Target = T;

    fn deref(&self) -> &T {
        // SAFETY: the guard exists, so this branch holds the lock.
        unsafe { &*self.lock.value.get() }
    }
}

impl<T> DerefMut for Guard<'_, T> {
    fn deref_mut(&mut self) -> &mut T {
        // SAFETY: as above, and &mut self is unique.
        unsafe { &mut *self.lock.value.get() }
    }
}

impl<T> Drop for Guard<'_, T> {
    fn drop(&mut self) {
        self.lock.locked.store(false, Ordering::Release);
    }
}

fn main() {
    let lock = SpinLock::new(0);
    thread::scope(|s| {
        for _ in 0..4 {
            s.spawn(|| {
                for _ in 0..1000 {
                    *lock.lock() += 1;
                }
            });
        }
    });
    println!("{}", *lock.lock());
}
```

```text
4000
```

Her satırın bir sebebi var:

| Satır | Neden |
|---|---|
| `T: Send` şartı | Değer kollar arasında gezer; `T: Sync` gerekmez |
| `compare_exchange_weak` | Döngüdeyiz, boşuna düşse de olur |
| `Acquire` | Kilit alınca önceki sahibin yazdıkları görünür |
| `Release` | Kilit bırakılınca yazdıklarımız görünür |
| `spin_loop` | İşlemciye "bekliyorum" der |
| `Guard` ve `Drop` | Kilit unutulamaz, panikte de açılır |
| `&mut self` değil `&self` | Paylaşılan değer kilitlenir |

Bu yapı `Mutex` ile aynı arayüzü verir. Peki neden hep `Mutex`?

## Neden spinlock kullanmamalı?

Spinlock beklerken işlemciyi boşuna döndürür. `Mutex` ise işletim sistemine "uyut" der.

| Durum | Spinlock | `Mutex` |
|---|---|---|
| Çok kısa iş, çok çekirdek | İyi | İyi |
| Uzun iş | Çekirdek boşa döner | Uyur |
| Kilit tutan kol zaman dilimi kaybederse | Herkes döner | Uyur |
| Çekirdeksiz yerler (`no_std`) | Tek seçenek olabilir | Yok |

Modern `Mutex` önce kısa süre döner, sonra uyur. Yani uygulama kodunda spinlock neredeyse hiç doğru cevap değildir. Burada onu nasıl çalıştığını görmek için yazdık.

## Kilitsiz yığın

Kilitsiz (lock-free) yapı, kol uyutulsa bile başkalarının ilerleyebildiği yapıdır. En basiti, başı atomik işaretçi olan bağlı listedir.

`push`: Yeni düğümün `next`'i eski başı göstersin, sonra başı `compare_exchange` ile değiştir. Araya başka kol girdiyse yeniden dene:

```rust
use std::ptr;
use std::sync::atomic::{AtomicPtr, Ordering};
use std::thread;

struct Node<T> {
    value: T,
    next: *mut Node<T>,
}

struct TakeStack<T> {
    head: AtomicPtr<Node<T>>,
}

// SAFETY: values move between branches, and the head is atomic.
unsafe impl<T: Send> Sync for TakeStack<T> {}

impl<T> TakeStack<T> {
    fn new() -> Self {
        TakeStack { head: AtomicPtr::new(ptr::null_mut()) }
    }

    fn push(&self, value: T) {
        let node = Box::into_raw(Box::new(Node { value, next: ptr::null_mut() }));
        let mut head = self.head.load(Ordering::Relaxed);
        loop {
            // SAFETY: the node is not shared yet.
            unsafe { (*node).next = head };
            let result = self.head.compare_exchange_weak(
                head,
                node,
                Ordering::Release,
                Ordering::Relaxed,
            );
            match result {
                Ok(_) => return,
                Err(actual) => head = actual,
            }
        }
    }

    fn take_all(&self) -> Vec<T> {
        let mut current = self.head.swap(ptr::null_mut(), Ordering::Acquire);
        let mut out = Vec::new();
        while !current.is_null() {
            // SAFETY: swap gave the whole chain to this branch alone.
            let node = unsafe { Box::from_raw(current) };
            current = node.next;
            out.push(node.value);
        }
        out
    }
}

impl<T> Drop for TakeStack<T> {
    fn drop(&mut self) {
        self.take_all();
    }
}

fn main() {
    let stack = TakeStack::new();
    thread::scope(|s| {
        for n in 0..4 {
            let stack = &stack;
            s.spawn(move || {
                for i in 0..100 {
                    stack.push(n * 1000 + i);
                }
            });
        }
    });
    let mut all = stack.take_all();
    all.sort();
    println!("{} {} {}", all.len(), all[0], all[399]);
    println!("{}", stack.take_all().len());
}
```

```text
400 0 3099
0
```

`take_all`, başı `swap` ile boşa çevirip bütün zinciri bir hamlede alır. Bu yüzden kimse silinen düğüme bakamaz.

## pop neden zor?

"Başı oku, `next`'ini al, başı `next` yap" kolay görünür. İki gerçek sorun var:

1. **Silinen bellek:** Başka kol düğümü `pop` edip silmiş olabilir; `next`'ini okumak tanımsız davranıştır.
2. **ABA:** Baş `A`, biz okuduk. Başka kol `A`'yı çıkardı, `B`'yi çıkardı, `A`'yı geri koydu. `compare_exchange` "hâlâ `A`" der ve başarılı olur, ama `next` artık yanlış.

Bu yüzden gerçek kilitsiz yapılar bellek geri kazanım şeması ister (hazard pointer, epoch). Kendi başına yazma: `crossbeam` gibi denenmiş bir crate kullan. `take_all` kalıbını seçmemizin sebebi tam bu ikisinden kaçınmasıdır.

## Özet

- Kilit: Atomik bayrak + `UnsafeCell` + `unsafe impl Sync` + `Guard`.
- `Acquire` alırken, `Release` bırakırken.
- Spinlock uygulama kodunda neredeyse hiç doğru değil; `Mutex`.
- Kilitsiz `push` kolaydır; `pop` silinen bellek ve ABA yüzünden zordur.
- Gerçek kilitsiz yapı için denenmiş crate.
