# Pin

İki bölümdür `self: Pin<&mut Self>` yazıyor, `pin!` ve `Box::pin` kullanıyor, "sebebini sonra göreceğiz" diyoruz. Sıra geldi. `Pin` tek bir soruna çözümdür: Kendini gösteren değerler.

## Taşınınca bozulan yapı

Rust'ta bir değeri taşımak, baytlarını başka yere kopyalamaktır. Çoğu zaman sorun olmaz. Ama bir yapının bir alanı aynı yapının başka alanını gösteriyorsa olur:

```rust
use std::{mem, ptr};

struct SelfRef {
    value: String,
    pointer: *const String,
}

impl SelfRef {
    fn new(text: &str) -> Self {
        SelfRef { value: text.to_string(), pointer: ptr::null() }
    }

    fn init(&mut self) {
        self.pointer = &self.value;
    }

    fn read(&self) -> &str {
        // SAFETY: a and b both stay alive until the end of main.
        unsafe { &*self.pointer }
    }
}

fn main() {
    let mut a = SelfRef::new("first");
    let mut b = SelfRef::new("second");
    a.init();
    b.init();
    println!("value {}, pointer reads {}", a.value, a.read());

    mem::swap(&mut a, &mut b);
    println!("value {}, pointer reads {}", a.value, a.read());
}
```

```text
value first, pointer reads first
value second, pointer reads first
```

`mem::swap` iki yapının baytlarını değiştirdi. `value` artık `second`, ama `pointer` hâlâ eski yeri gösteriyor ve `first` okuyor. Yapı kendi içinde tutarsız kaldı. Burada iki yapı da yaşadığı için yalnızca yanlış değer okuduk; biri düşmüş olsaydı tanımsız davranış olurdu.

Olağan Rust'ta bu yapıyı referansla yazamazsın, ödünç alma denetleyicisi izin vermez. Biz ham işaretçiyle yazdık.

## async fn de böyle bir yapıdır

Şu masum koda bak:

```rust
async fn holds() -> u32 {
    let value = 5;
    let reference = &value;
    pause().await;
    *reference + 1
}

fn main() {
    println!("{}", block_on(holds()));
}
```

```text
6
```

Geçen bölümlerde gördük: `.await`'i aşan değişkenler durum makinesinin içinde saklanır. `value` da `reference` da aynı future'ın içinde duruyor, yani **`reference` kendi yapısının bir alanını gösteriyor**. Future `.await`'te beklerken taşınırsa `reference` eski adresi gösterir.

Yani iki seçenek vardı: `.await`'i aşan referansları yasaklamak ya da yoklanmaya başlayan future'ın taşınmayacağını garanti etmek. Rust ikincisini seçti.

İlk yoklamadan önce taşımak sorun değildir, çünkü gövde henüz çalışmadı, içeride referans yok. Bu yüzden `async fn` çağrısının sonucunu serbestçe taşıyabiliyoruz. Yoklamaya başlarken söz gerekir.

## Pin: Taşımayacağım sözü

`Pin<P>` bir işaretçiyi saran türdür. Tek bir şey söyler: **Gösterilen değer, düşene kadar yerinden taşınmayacak.**

Çalışma zamanında hiçbir şey yapmaz:

```rust
use std::pin::Pin;

fn main() {
    println!("{}", size_of::<Pin<&mut u64>>() == size_of::<&mut u64>());
    println!("{}", size_of::<Pin<Box<u64>>>() == size_of::<Box<u64>>());
}
```

```text
true
true
```

Bütün iş tür düzeyindedir. Taşımak için değere sahip olmak ya da `&mut T` gerekir (`mem::swap` böyle çalışır). `Pin<&mut T>` sana o `&mut T`'yi vermez. Erişemediğin şeyi taşıyamazsın.

Dikkat: Sabit olan **gösterilen değerdir**, işaretçinin kendisi değil. `Pin<Box<T>>`'yi istediğin yere taşıyabilirsin; kutu taşınır, içindeki değer yerinde kalır.

## Unpin: "Benim için fark etmez"

Çoğu tür kendini göstermez; onları taşımak her zaman güvenlidir. Bunlar için bütün bu törene gerek yok. `Unpin` bunu söyleyen trait'tir. `Send` gibi otomatik uygulanır:

```rust
use std::marker::PhantomPinned;
use std::pin::Pin;

fn needs_unpin<T: Unpin>() {}

fn main() {
    needs_unpin::<i32>();
    needs_unpin::<String>();
    needs_unpin::<Vec<u8>>();
    needs_unpin::<Box<PhantomPinned>>();
    needs_unpin::<Pin<Box<PhantomPinned>>>();
    println!("all of them are Unpin");
}
```

```text
all of them are Unpin
```

`Box<PhantomPinned>` ve `Pin<Box<...>>` de `Unpin`, çünkü taşınan yalnızca işaretçidir.

Tür `Unpin` ise `Pin` etkisizdir: `Pin::new` ile sabitler, `get_mut` ile `&mut T` geri alırsın. Geçen bölümlerde `Countdown` gibi sade yapılarda bu yüzden hiç zorlanmadık.

`async fn` future'ı ise `Unpin` **değildir**:

```rust
use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Waker};

async fn pause() {}

async fn holds() -> u32 {
    let value = 5;
    let reference = &value;
    pause().await;
    *reference + 1
}

fn main() {
    let mut future = holds();
    let mut cx = Context::from_waker(Waker::noop());
    let _ = Pin::new(&mut future).poll(&mut cx);
}
```

```text
error[E0277]: `{async fn body of holds()}` cannot be unpinned
  --> main.rs:17:22
   |
 7 | async fn holds() -> u32 {
   |                     --- within this `impl Future<Output = u32>`
...
17 |     let _ = Pin::new(&mut future).poll(&mut cx);
   |             -------- ^^^^^^^^^^^ within `impl Future<Output = u32>`, the trait
   `Unpin` is not implemented for `{async fn body of holds()}`
   |             |
   |             required by a bound introduced by this call
   |
   = note: consider using the `pin!` macro
           consider using `Box::pin` if you need to access the pinned value outside of
           the current scope
note: required because it appears within the type `impl Future<Output = u32>`
  --> main.rs:7:21
   |
 7 | async fn holds() -> u32 {
   |                     ^^^
note: required by a bound in `Pin::<Ptr>::new`
```

Derleyici yanlış kullanımı burada durduruyor. Kural basit: Geçen bölümlerde `Join`'in neden `Unpin` istediğinin ve `async fn` future'larını neden `Box::pin` ile sardığımızın cevabı bu.

## Sabitlemenin iki yolu

```rust
async fn work(name: &str) -> String {
    pause().await;
    format!("{name} finished")
}

fn main() {
    let mut cx = Context::from_waker(Waker::noop());

    let mut on_stack = pin!(work("stack"));
    while on_stack.as_mut().poll(&mut cx).is_pending() {}

    let mut on_heap = Box::pin(work("heap"));
    let result = loop {
        if let Poll::Ready(text) = on_heap.as_mut().poll(&mut cx) {
            break text;
        }
    };
    println!("{result}");
}
```

```text
heap finished
```

| Yol | Nerede durur | Ne zaman |
|---|---|---|
| `pin!(f)` | Bulunduğu kapsamda | Kapsam içinde bitecekse; ayırma yok |
| `Box::pin(f)` | Yığında (heap) | Kapsamdan uzun yaşayacaksa ya da taşınacaksa (görevler) |

`pin!`, değeri kendi içine taşır. Özgün değişken artık kullanılamaz, yani sözü bozmanın yolu kalmaz.

## Güvenli kendini gösteren yapı

Baştaki yapıyı doğru yazalım. `PhantomPinned` yapıyı `Unpin` olmaktan çıkaran, boyutu sıfır bir alandır:

```rust
use std::marker::PhantomPinned;
use std::pin::Pin;
use std::ptr;

struct SelfRef {
    value: String,
    pointer: *const String,
    _pin: PhantomPinned,
}

impl SelfRef {
    fn new(text: &str) -> Pin<Box<Self>> {
        let mut boxed = Box::pin(SelfRef {
            value: text.to_string(),
            pointer: ptr::null(),
            _pin: PhantomPinned,
        });
        let pointer: *const String = &boxed.value;
        // SAFETY: writing a field does not move the struct.
        unsafe { boxed.as_mut().get_unchecked_mut().pointer = pointer };
        boxed
    }

    fn read(self: Pin<&Self>) -> &str {
        // SAFETY: the struct is pinned, so the pointer still shows its field.
        unsafe { &*self.pointer }
    }
}

fn main() {
    let mut a = SelfRef::new("first");
    let mut b = SelfRef::new("second");
    std::mem::swap(&mut a, &mut b);
    println!("value {}, pointer reads {}", a.value, a.as_ref().read());
}
```

```text
value second, pointer reads second
```

Aynı `mem::swap`, ama artık kutuları takas ediyor; içerik yerinde kaldı ve değer ile işaretçi tutarlı. Yapı `Unpin` olmadığı için `pointer` alanını yazarken `get_unchecked_mut` gerekti.

Değeri `&mut` ile almaya kalkarsak:

```rust
use std::marker::PhantomPinned;

struct Stuck {
    value: u32,
    _pin: PhantomPinned,
}

fn main() {
    let mut boxed = Box::pin(Stuck { value: 1, _pin: PhantomPinned });
    let stuck: &mut Stuck = boxed.as_mut().get_mut();
    stuck.value = 2;
}
```

```text
error[E0277]: `PhantomPinned` cannot be unpinned
  --> main.rs:10:44
   |
10 |     let stuck: &mut Stuck = boxed.as_mut().get_mut();
   |                                            ^^^^^^^ within `Stuck`, the trait
   `Unpin` is not implemented for `PhantomPinned`
   |
   = note: consider using the `pin!` macro
           consider using `Box::pin` if you need to access the pinned value outside of
           the current scope
note: required because it appears within the type `Stuck`
  --> main.rs:3:8
   |
 3 | struct Stuck {
   |        ^^^^^
note: required by a bound in `Pin::<&'a mut T>::get_mut`
```

## Alan sabitleme: İç future'ı yoklamak

Asıl pratik mesele şu: Bir future'ı saran bir future yazıyorsun, iç future `Unpin` değil. Elinde `Pin<&mut Self>` var, sana `Pin<&mut F>` lazım. Buna **alan sabitleme** (pin projection) denir:

```rust
struct Counted<F> {
    inner: F,
    polls: u32,
}

impl<F: Future> Future for Counted<F> {
    type Output = F::Output;

    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<F::Output> {
        // SAFETY: inner is never moved out of self.
        let this = unsafe { self.get_unchecked_mut() };
        this.polls += 1;
        // SAFETY: self is pinned, so its inner field stays in place too.
        let inner = unsafe { Pin::new_unchecked(&mut this.inner) };
        inner.poll(cx)
    }
}

async fn two_pauses() -> u32 {
    pause().await;
    pause().await;
    7
}

fn main() {
    let mut future = pin!(Counted { inner: two_pauses(), polls: 0 });
    let mut cx = Context::from_waker(Waker::noop());
    let value = loop {
        if let Poll::Ready(value) = future.as_mut().poll(&mut cx) {
            break value;
        }
    };
    println!("value {value}, polls {}", future.polls);
}
```

```text
value 7, polls 3
```

İki `unsafe` var, ikisinde de söz biziz:

- `get_unchecked_mut`: "`self`'i taşımayacağım."
- `Pin::new_unchecked`: "`inner`'ı da taşımayacağım; `self` sabitse alanı da sabittir."

`polls` ise sabitlenmedi: Düz `&mut` ile değiştirdik, çünkü onun taşınması önemsiz. Her alan için ayrı karar verilir:

| Alan | Karar | Erişim |
|---|---|---|
| İç future | Sabitlenir | `Pin::new_unchecked(&mut this.inner)` |
| Sayaç, bayrak, sonuç | Sabitlenmez | `&mut this.alan`, taşınabilir |

Artık `Join`'i `Unpin` şartı ve `Box::pin` olmadan yazabilirsin; alıştırmalardan biri tam bu. Gerçek projede bu `unsafe`'leri elle yazmak yerine `pin-project` crate'i kullanılır, aynısını makroyla üretir.

## Özet

- Taşımak baytları kopyalamaktır; kendini gösteren yapı taşınınca bozulur.
- `.await`'i aşan referans future'ı kendini gösteren bir yapı yapar.
- `Pin<P>`: Gösterilen değer düşene kadar taşınmayacak. Çalışma zamanı bedeli yok.
- `Unpin`: Sabitlemenin önemi olmayan türler; çoğu tür. `async fn` future'ı değil.
- `pin!` kapsamda, `Box::pin` yığında sabitler.
- Alan sabitleme: İç future `Pin::new_unchecked`, sıradan alanlar düz `&mut`.

Async'in temel taşları böylece tamam: `Future`, waker, çalıştırıcı ve `Pin`.
