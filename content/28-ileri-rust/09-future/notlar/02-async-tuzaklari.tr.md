## .await'i unutmak

Future tembeldir; çağırıp bırakırsan hiçbir şey olmaz. Derleyici neyse ki uyarır:

```rust
async fn save() {}

fn main() {
    save();
}
```

```text
warning: unused implementer of `Future` that must be used
 --> main.rs:4:5
  |
4 |     save();
  |     ^^^^^^
  |
  = note: futures do nothing unless you `.await` or poll them
  = note: `#[warn(unused_must_use)]` (part of `#[warn(unused)]`) on by default
```

## async dışında .await

Yoklayacak bir dış future yoksa `.await` yazılamaz:

```rust
fn main() {
    let value = std::future::ready(1).await;
    println!("{value}");
}
```

```text
error[E0728]: `await` is only allowed inside `async` functions and blocks
 --> main.rs:2:39
  |
1 | fn main() {
  | --------- this is not `async`
2 |     let value = std::future::ready(1).await;
  |                                       ^^^^^ only allowed inside `async` functions
  and blocks
```

`main`'i `async` yapmak da çözmez, çünkü onu yoklayan biri olmaz. Çözüm bir çalıştırıcı: `block_on(future)`.

## Kendini çağıran async fn

Durum makinesi kendini içerseydi boyutu sonsuz olurdu:

```rust
async fn count_down(n: u32) {
    if n > 0 {
        count_down(n - 1).await;
    }
}

fn main() {
    let _ = count_down(2);
}
```

```text
error[E0733]: recursion in an async fn requires boxing
 --> main.rs:1:1
  |
1 | async fn count_down(n: u32) {
  | ^^^^^^^^^^^^^^^^^^^^^^^^^^^
2 |     if n > 0 {
3 |         count_down(n - 1).await;
  |         ----------------------- recursive call here
  |
  = note: a recursive `async fn` call must introduce indirection such as `Box::pin` to
    avoid an infinitely sized future
```

Çözüm, iç çağrıyı yığına koymak. Yapının içinde artık yalnızca bir işaretçi kalır:

```rust
async fn count_down(n: u32) {
    if n > 0 {
        println!("{n}");
        Box::pin(count_down(n - 1)).await;
    }
}

fn main() {
    block_on(count_down(2));
}
```

```text
2
1
```

## Bitmiş future'ı yeniden yoklamak

`Ready` döndüren future'ın işi bitmiştir. Yeniden yoklamak sözleşmeye aykırıdır ve `async fn` future'ı panikler:

```rust
async fn one() -> u32 {
    1
}

fn main() {
    let mut future = pin!(one());
    let mut cx = Context::from_waker(Waker::noop());
    println!("{:?}", future.as_mut().poll(&mut cx));
    println!("{:?}", future.as_mut().poll(&mut cx));
}
```

```text
Ready(1)

thread 'main' panicked at main.rs:4:23:
`async fn` resumed after completion
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

Elle `Join` yazarken biten future'ı bir daha yoklamamak bu yüzden gerekir.

## Kolu bloklamak

`async` gövdede `thread::sleep`, uzun hesap ya da bloklayan dosya okuma bütün kolu durdurur. Dersteki `Yield`'siz örnekte olan buydu: Sıra hiç dönmedi. Kural basit: `.await` yoksa sıra da yok.

## Pending dönüp haber vermemek

`cx.waker().wake_by_ref()` çağırmadan `Pending` döndürmek bizim boşa dönen `block_on`'umuzda fark edilmez, çünkü o zaten hep yeniden sorar. Uyuyan gerçek bir çalıştırıcıda future bir daha hiç yoklanmaz ve program sessizce asılı kalır. Bunu 10. bölümde göreceğiz.
