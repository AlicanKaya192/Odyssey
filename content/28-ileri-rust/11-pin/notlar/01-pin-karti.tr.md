## Araçlar

| Ad | Ne işe yarar | Şart |
|---|---|---|
| `Pin::new(&mut t)` | Sabitler | `T: Unpin` |
| `pin!(f)` | Kapsamda sabitler | Yok |
| `Box::pin(f)` | Yığında (heap) sabitler | Yok |
| `pinned.as_mut()` | `Pin<&mut T>`'yi yeniden ödünç alır | Yok |
| `pinned.as_ref()` | `Pin<&T>` verir | Yok |
| `pinned.get_mut()` | `&mut T` verir | `T: Unpin` |
| `pinned.get_unchecked_mut()` | `&mut T` verir | `unsafe` |
| `Pin::new_unchecked(p)` | Sabitler | `unsafe` |

## Hangi tür Unpin?

| Tür | `Unpin`? |
|---|---|
| `i32`, `String`, `Vec<T>` | Evet |
| Yalnızca `Unpin` alanları olan yapı | Evet |
| `Box<T>` | Evet, `T` ne olursa olsun |
| `Pin<Box<T>>` | Evet, `T` ne olursa olsun |
| `async fn` ve `async` blok future'ı | Hayır |
| `PhantomPinned` alanlı yapı | Hayır |

## Karar tablosu

| Durum | Yap |
|---|---|
| Sade yapı için `Future` yazıyorsun | `mut self: Pin<&mut Self>`, `self.alan` |
| İç future'lar `Unpin` | `self.get_mut()`, `Pin::new(&mut this.ic)` |
| İç future `Unpin` değil | Alan sabitleme |
| `async fn`'i yerinde yokluyorsun | `pin!` |
| Future'ı saklayıp taşıyorsun | `Box::pin` |
| Farklı future'ları bir arada tutuyorsun | `Pin<Box<dyn Future<...>>>` |

## Sık hata

Aynı `Pin<&mut F>` iki kez kullanılamaz, çünkü `poll` onu tüketir:

```rust
use std::future::Future;
use std::pin::pin;
use std::task::{Context, Waker};

async fn pause() {}

fn main() {
    let future = pin!(pause());
    let mut cx = Context::from_waker(Waker::noop());
    let _ = future.poll(&mut cx);
    let _ = future.poll(&mut cx);
}
```

```text
error[E0382]: use of moved value: `future`
  --> main.rs:11:13
   |
 8 |     let future = pin!(pause());
   |         ------ move occurs because `future` has type `Pin<&mut impl Future<Output =
   ()>>`, which does not implement the `Copy` trait
 9 |     let mut cx = Context::from_waker(Waker::noop());
10 |     let _ = future.poll(&mut cx);
   |                    ------------- `future` moved due to this method call
11 |     let _ = future.poll(&mut cx);
   |             ^^^^^^ value used here after move
   |
note: `std::future::Future::poll` takes ownership of the receiver `self`, which moves
`future`
help: consider reborrowing the `Pin` instead of moving it
   |
10 |     let _ = future.as_mut().poll(&mut cx);
   |                   +++++++++
```

Düzeltme: Her yoklamada `future.as_mut().poll(&mut cx)`, değişken de `let mut future`.
