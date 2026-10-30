# Send ve Sync

Rust'ın veri yarışını derlerken durdurmasının sebebi iki küçük trait'tir. Yöntemleri yoktur, yalnızca bir söz taşırlar. Derleyici çoğu türe kendiliğinden verir, gerisini biz yazarız.

## İki söz

| Trait | Sözü | Olmayan örnek |
|---|---|---|
| `Send` | Sahiplik başka kola geçebilir | `Rc<T>` |
| `Sync` | `&T` kollar arasında paylaşılabilir | `Cell<T>`, `RefCell<T>` |

İkisi arasındaki bağ şudur: `T: Sync` demek, `&T: Send` demektir. Paylaşmak, referansı göndermektir.

Bir türün hangisi olduğunu denemek için boş bir fonksiyon yeter:

```rust
use std::cell::Cell;
use std::sync::{Arc, Mutex};

fn assert_send<T: Send>() {}
fn assert_sync<T: Sync>() {}

fn main() {
    assert_send::<i32>();
    assert_send::<String>();
    assert_send::<Cell<i32>>();
    assert_sync::<Arc<i32>>();
    assert_sync::<Mutex<Cell<i32>>>();
    println!("all passed");
}
```

```text
all passed
```

Program çalıştıysa bu türlerin hepsi şartı sağlıyor demektir. `Rc` için derlenmez:

```rust
use std::rc::Rc;

fn assert_send<T: Send>() {}

fn main() {
    assert_send::<Rc<i32>>();
}
```

```text
error[E0277]: `Rc<i32>` cannot be sent between threads safely
 --> main.rs:6:19
  |
6 |     assert_send::<Rc<i32>>();
  |                   ^^^^^^^ `Rc<i32>` cannot be sent between threads safely
  |
  = help: the trait `Send` is not implemented for `Rc<i32>`
note: required by a bound in `assert_send`
 --> main.rs:3:19
  |
3 | fn assert_send<T: Send>() {}
  |                   ^^^^ required by this bound in `assert_send`
```

## Kendiliğinden gelir

Bir struct'ın bütün alanları `Send` ise struct da `Send`'dir. Bu yüzden bunlara **otomatik trait** denir. Her zamanki türlerde hiç düşünmezsin. Zinciri bozan birkaç tür vardır:

| Tür | `Send` | `Sync` | Neden |
|---|---|---|---|
| `i32`, `String`, `Vec<T>` | Evet | Evet | Sıradan sahiplik |
| `Rc<T>` | Hayır | Hayır | Sayaç atomik değil |
| `Cell<T>`, `RefCell<T>` | Evet | Hayır | `&` üzerinden kilitsiz yazar |
| `Arc<T>` | `T: Send + Sync` | `T: Send + Sync` | Atomik sayaç, içi paylaşılır |
| `Mutex<T>` | `T: Send` | `T: Send` | Kilit erişimi sıraya sokar |
| `*const T`, `*mut T`, `NonNull<T>` | Hayır | Hayır | Derleyici arkasını bilmez |
| `MutexGuard<T>` | Hayır | `T: Sync` | Kilit aynı kolda açılmalı |

`Mutex<T>`'nin şartı dikkat çeker: `T: Sync` istemez, çünkü kilit aynı anda tek erişim sağlar; `RefCell` içeren değer bile `Mutex` içinde paylaşılabilir. Ama `T: Send` ister, çünkü değer kollar arasında gezer.

## Kendi türünde

Ham işaretçi tutan tür kendiliğinden `Send` olmaz. Önceki bölümdeki `MyVec` kola geçmez:

```rust
fn main() {
    let list = MyVec::from_one(5);
    let handle = thread::spawn(move || println!("{}", list.first()));
    handle.join().unwrap();
}
```

```text
error[E0277]: `NonNull<i32>` cannot be sent between threads safely
  --> main.rs:30:32
   |
30 |     let handle = thread::spawn(move || println!("{}", list.first()));
   |                  ------------- -------^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   |                  |             |
   |                  |             `NonNull<i32>` cannot be sent between threads safely
   |                  |             within this `{closure@main.rs:30:32: 30:39}`
   |                  required by a bound introduced by this call
   |
   = help: within `{closure@main.rs:30:32: 30:39}`, the trait `Send` is not implemented
     for `NonNull<i32>`
note: required because it appears within the type `MyVec<i32>`
  --> main.rs:4:8
   |
 4 | struct MyVec<T> {
   |        ^^^^^
note: required because it's used within this closure
  --> main.rs:30:32
   |
30 |     let handle = thread::spawn(move || println!("{}", list.first()));
   |                                ^^^^^^^
note: required by a bound in `spawn`
```

Bu kısıtlama fazla katıdır: `MyVec` öğelerine sahiptir, aynen `Vec` gibi. Söz vermek bize düşer:

```rust
// SAFETY: MyVec owns its items, like Vec.
unsafe impl<T: Send> Send for MyVec<T> {}
// SAFETY: &MyVec gives only &T.
unsafe impl<T: Sync> Sync for MyVec<T> {}

fn main() {
    let list = MyVec::from_one(5);
    let handle = thread::spawn(move || println!("{} {}", list.first(), list.len));
    handle.join().unwrap();
}
```

```text
5 1
```

`unsafe impl` diyor ki: "Bu sözü derleyici kanıtlayamıyor, ben garanti ediyorum." Şartı doğru yazmak şart: `T: Send` olmadan yazsaydık `MyVec<Rc<i32>>` da kola geçerdi ve sayaç yarışırdı.

## Yanlış söz

Derleyici yanlış `unsafe impl`'i yakalamaz:

```rust
struct MyRc(Rc<i32>);

// WRONG: the counter inside is not atomic.
unsafe impl Send for MyRc {}
```

Bu derlenir. İki kol kopyalayıp düşürdükçe sayaç bozulur, değer erken silinir ya da hiç silinmez. Sonuç veri yarışı, yani tanımsız davranış. `unsafe impl Send` yazmadan önce sorulacak soru: **"Bu türün bütün değişen durumu ya sahipli ya da eşzamanlı olarak güvenli mi?"**

## Ters yön: Sözü geri almak

Tür `Send` olmamalıysa `PhantomData` ile söz geri alınır:

```rust
use std::marker::PhantomData;

struct Local {
    value: i32,
    _not_send: PhantomData<*const ()>,
}

fn main() {
    let local = Local { value: 3, _not_send: PhantomData };
    println!("{} {}", local.value, size_of::<Local>());
}
```

```text
3 4
```

İşletim sistemi kaynağı aynı kolda kapatılması gereken türlerde kullanılır. `PhantomData<*const ()>` hiç yer tutmaz, ama ham işaretçi olduğu için `Send` ve `Sync`'i düşürür.

## UnsafeCell: Her şeyin altındaki tür

`&T` üzerinden değer değiştirmek normalde tanımsız davranıştır. Tek istisna `UnsafeCell<T>`'dir. `Cell`, `RefCell`, `Mutex` ve atomiklerin hepsi onun üstüne kuruludur:

```rust
use std::cell::UnsafeCell;

struct MyCell<T> {
    value: UnsafeCell<T>,
}

impl<T: Copy> MyCell<T> {
    fn new(value: T) -> Self {
        MyCell { value: UnsafeCell::new(value) }
    }

    fn get(&self) -> T {
        // SAFETY: MyCell is not Sync and gives no references, so no one else reads now.
        unsafe { *self.value.get() }
    }

    fn set(&self, value: T) {
        // SAFETY: as above.
        unsafe { *self.value.get() = value };
    }
}

fn main() {
    let cell = MyCell::new(1);
    let a = &cell;
    let b = &cell;
    a.set(2);
    b.set(b.get() + 1);
    println!("{}", cell.get());
}
```

```text
3
```

`UnsafeCell` `Sync` değildir, bu yüzden `MyCell` da kendiliğinden `Sync` olmaz: `set` kollar arasında çağrılamaz. Doğru davranış, ek çaba gerektirmeden geldi. Kilit bölümünde aynı türü `unsafe impl Sync` ile paylaşılabilir yapacağız.

## Özet

- `Send`: Sahiplik geçer. `Sync`: `&T` paylaşılır.
- Alanlardan kendiliğinden hesaplanır; ham işaretçi zinciri keser.
- `unsafe impl<T: Send> Send for X<T> {}`: Şart yazmadan yazma.
- Yanlış `unsafe impl` derlenir ve veri yarışı üretir.
- `PhantomData<*const ()>` sözü geri alır.
- `UnsafeCell`, `&` üzerinden yazmanın tek yasal yolu.
