# Genel Tekrar

Bu modül Rust'ı "kullanmak"tan "altında ne olduğunu bilmek"e taşıdı. Bu bölüm yeni bir şey öğretmiyor, parçaları birleştiriyor. Sınav ve alıştırmalar da böyle: Her soru başka bir bölümden.

## Tek programda modül

Aşağıdaki program modülün çoğunu kullanıyor. Her satırı açıklayabiliyorsan bu modül tamamdır:

```rust
use std::alloc::{Layout, alloc, dealloc};
use std::future::Future;
use std::pin::{Pin, pin};
use std::ptr;
use std::sync::atomic::{AtomicU32, Ordering};
use std::task::{Context, Poll, Waker};

static POLLS: AtomicU32 = AtomicU32::new(0);

struct Pause(bool);

impl Future for Pause {
    type Output = ();

    fn poll(mut self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<()> {
        POLLS.fetch_add(1, Ordering::Relaxed);
        if self.0 {
            return Poll::Ready(());
        }
        self.0 = true;
        cx.waker().wake_by_ref();
        Poll::Pending
    }
}

struct RawBox {
    pointer: *mut u32,
}

impl RawBox {
    fn new(value: u32) -> Self {
        let layout = Layout::new::<u32>();
        // SAFETY: u32 has a non-zero size.
        let pointer = unsafe { alloc(layout) }.cast::<u32>();
        assert!(!pointer.is_null());
        // SAFETY: the pointer is valid and aligned for a u32.
        unsafe { ptr::write(pointer, value) };
        RawBox { pointer }
    }

    fn get(&self) -> u32 {
        // SAFETY: new wrote a value, and drop has not run.
        unsafe { *self.pointer }
    }
}

impl Drop for RawBox {
    fn drop(&mut self) {
        // SAFETY: the pointer came from alloc with the same layout.
        unsafe { dealloc(self.pointer.cast(), Layout::new::<u32>()) };
    }
}

macro_rules! total {
    ($($x:expr),* $(,)?) => { 0 $(+ $x)* };
}

async fn work() -> u32 {
    let held = RawBox::new(40);
    Pause(false).await;
    total!(held.get(), 1, 1)
}

fn main() {
    let mut future = pin!(work());
    let mut cx = Context::from_waker(Waker::noop());
    let value = loop {
        if let Poll::Ready(value) = future.as_mut().poll(&mut cx) {
            break value;
        }
    };
    println!("{value} after {} polls", POLLS.load(Ordering::Relaxed));
}
```

```text
42 after 2 polls
```

| Yer | Konu |
|---|---|
| `alloc`, `dealloc`, `ptr::write` | Kendi bellek yönetimin, `Layout` |
| `// SAFETY:` | `unsafe`'in gerekçesi |
| `Drop for RawBox` | Sahipliği ham işaretçiye taşımak |
| `AtomicU32`, `Ordering::Relaxed` | Atomikler |
| `impl Future for Pause` | Elle future, `Poll`, waker |
| `async fn work` | Durum makinesi; `held` `.await`'i aşıyor, future'ın içinde duruyor |
| `pin!`, `Waker::noop` | Sabitleme, en küçük çalıştırıcı |
| `macro_rules! total` | Tekrar kalıbı |

## En önemli dört fikir

**1. `unsafe` söz vermektir.** Denetimleri kapatmaz, derleyicinin kanıtlayamadığını senin üstlenmeni ister. Çağıran da bu sözün farkında olmalıdır:

```rust
unsafe fn read(pointer: *const u32) -> u32 {
    unsafe { *pointer }
}

fn main() {
    let value = 1;
    println!("{}", read(&value));
}
```

```text
error[E0133]: call to unsafe function `read` is unsafe and requires unsafe block
 --> main.rs:7:20
  |
7 |     println!("{}", read(&value));
  |                    ^^^^^^^^^^^^ call to unsafe function
  |
  = note: consult the function's documentation for information on how to avoid undefined
    behavior
```

En iyi `unsafe`, küçük bir yere kapatılmış ve dışarıya güvenli bir arayüzle açılmış olandır. Daha da iyisi, sözü türe yazmaktır: Bitirme projesindeki `Producer` gibi.

**2. `Send` ve `Sync` kolları türle güvenli yapar.** Veri yarışı çalışma zamanı sürprizi değil, derleme hatasıdır:

```rust
use std::cell::Cell;
use std::thread;

fn main() {
    let shared = Cell::new(1);
    thread::scope(|s| {
        s.spawn(|| shared.set(2));
    });
}
```

```text
error[E0277]: `Cell<i32>` cannot be shared between threads safely
 --> main.rs:7:17
  |
7 |         s.spawn(|| shared.set(2));
  |           ----- ^^^^^^^^^^^^^^^^ `Cell<i32>` cannot be shared between threads safely
  |           |
  |           required by a bound introduced by this call
  |
  = help: the trait `Sync` is not implemented for `Cell<i32>`
  = note: if you want to do aliasing and mutation between multiple threads, use
    `std::sync::RwLock` or `std::sync::atomic::AtomicI32` instead
  = note: required for `&Cell<i32>` to implement `Send`
note: required because it's used within this closure
 --> main.rs:7:17
  |
7 |         s.spawn(|| shared.set(2));
  |                 ^^
note: required by a bound in `Scope::<'scope, 'env>::spawn`
```

**3. Future bir durum makinesidir.** Kendi kendine çalışmaz, yoklanır. `.await` beklemez, `Pending`'i yukarı iletir. Haber vermeyen future sessizce asılı kalır.

**4. Taşımak bayt kopyalamaktır, `Pin` bu yüzden var.** Kendini gösteren değer taşınınca bozulur. `async fn` böyle bir değerdir ve derleyici yanlış kullanımı durdurur:

```rust
use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Waker};

async fn work() {}

fn main() {
    let mut future = work();
    let mut cx = Context::from_waker(Waker::noop());
    let _ = Pin::new(&mut future).poll(&mut cx);
}
```

```text
error[E0277]: `{async fn body of work()}` cannot be unpinned
  --> main.rs:10:22
   |
 5 | async fn work() {}
   |                - within this `impl Future<Output = ()>`
...
10 |     let _ = Pin::new(&mut future).poll(&mut cx);
   |             -------- ^^^^^^^^^^^ within `impl Future<Output = ()>`, the trait
   `Unpin` is not implemented for `{async fn body of work()}`
   |             |
   |             required by a bound introduced by this call
   |
   = note: consider using the `pin!` macro
           consider using `Box::pin` if you need to access the pinned value outside of
           the current scope
note: required because it appears within the type `impl Future<Output = ()>`
  --> main.rs:5:16
   |
 5 | async fn work() {}
   |                ^
note: required by a bound in `Pin::<Ptr>::new`
```

## Kısa özet

| Bölüm | Bir cümle |
|---|---|
| `unsafe`, ham işaretçi | Beş ek yetki, denetimler sürer |
| Bellek düzeni, `MaybeUninit` | Boyut, hizalama, kurulmamış bellek |
| Kendi `Vec`'in | `alloc`, `realloc`, `Drop` bir arada |
| `PhantomData`, varyans | Ömürlerin türlerle ilişkisi |
| `Send`, `Sync`, atomikler | Kol güvenliği ve bellek sırası |
| Spinlock, kilitsiz yapılar | Kolay görünen zor iş |
| `Future`, çalıştırıcı | Yoklama, waker, görev kuyruğu |
| `Pin` | Taşınmama sözü |
| Makrolar | Derlemede kod üretmek |
| FFI | C ile konuşmak, sınırda sahiplik |
| `no_std` | `core`, `alloc`, `std` katmanları |
| Performans | Önce ölç |

Takıldığın konu olursa sınavın sonundaki bağlantılar seni o bölüme götürür.
