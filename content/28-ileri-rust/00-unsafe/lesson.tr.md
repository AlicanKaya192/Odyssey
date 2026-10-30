# unsafe Ne Demek

Derleyici bir programı ancak kanıtlayabilirse kabul eder. Bazı doğru programları kanıtlayamaz. `Vec` ve `Mutex` gibi temel türler de bu yüzden içeride `unsafe` kullanır. Bu modül o katmanı açıyor.

`unsafe`, "kuralları kapat" demek değildir. **"Bu kısmın doğru olduğunu derleyici değil, ben garanti ediyorum"** demektir.

## Beş yetki

`unsafe` blok, yalnızca şu beş işe izin verir:

| Yetki | Örnek |
|---|---|
| Ham işaretçinin gösterdiğini okumak ya da yazmak | `*p` |
| `unsafe fn` çağırmak | `v.get_unchecked(0)` |
| `static mut` değişkene ulaşmak | `COUNT += 1` |
| `unsafe trait` uygulamak | `unsafe impl Send for T {}` |
| `union` alanı okumak | `u.number` |

Ham işaretçi `*const T` ya da `*mut T` yazılır. Onu **üretmek** güvenlidir, gösterdiğini **okumak** değil:

```rust
fn main() {
    let value = 5;
    let p = &value as *const i32;

    // SAFETY: p comes from a reference to value, which is alive here.
    let read = unsafe { *p };
    println!("{read}");
}
```

```text
5
```

Blok olmadan derlenmez:

```rust
fn main() {
    let value = 5;
    let p = &value as *const i32;
    let read = *p;
    println!("{read}");
}
```

```text
error[E0133]: dereference of raw pointer is unsafe and requires unsafe block
 --> main.rs:4:16
  |
4 |     let read = *p;
  |                ^^ dereference of raw pointer
  |
  = note: raw pointers may be null, dangling or unaligned; they can violate aliasing
    rules and cause data races: all of these are undefined behavior
```

## unsafe neyi kapatmaz?

Tür denetimi, sahiplik ve ödünç kuralları `unsafe` içinde de geçerlidir:

```rust
fn main() {
    let mut n = 1;
    unsafe {
        let a = &mut n;
        let b = &mut n;
        *a += 1;
        *b += 1;
    }
    println!("{n}");
}
```

```text
warning: unnecessary `unsafe` block
 --> main.rs:3:5
  |
3 |     unsafe {
  |     ^^^^^^ unnecessary `unsafe` block
  |
  = note: `#[warn(unused_unsafe)]` (part of `#[warn(unused)]`) on by default

error[E0499]: cannot borrow `n` as mutable more than once at a time
 --> main.rs:5:17
  |
4 |         let a = &mut n;
  |                 ------ first mutable borrow occurs here
5 |         let b = &mut n;
  |                 ^^^^^^ second mutable borrow occurs here
6 |         *a += 1;
  |         ------- first borrow later used here
```

`unsafe`, yeni yetkiler ekler; var olan denetimleri kaldırmaz. İşaretçi kullanınca denetim dışına çıkılır, çünkü ham işaretçinin ömrü yoktur.

## Tanımsız davranış

`unsafe` içinde kuralı bozarsan sonuç **hata** değil, **tanımsız davranış** (undefined behavior) olur: Dil, programın ne yapacağına dair hiçbir söz vermez.

| Yapılan | Neden tanımsız |
|---|---|
| Boş ya da silinmiş belleği okumak | İşaretçi geçerli değil |
| Sınır dışına erişmek | Başka veriyi okur |
| Aynı anda iki `&mut` | Derleyici tek olduğunu varsayarak iyileştirir |
| `bool`'a `2` yazmak | Tür yalnızca 0 ve 1 olabilir |
| Veri yarışı | Sonuç kola göre değişir |

En tehlikeli yanı: **Program çalışıyor görünebilir.** Bugün geçen test yarın derleyici sürümü değişince düşebilir. Bu yüzden `unsafe` deneyerek doğrulanmaz, **gerekçeyle** doğrulanır.

Aynı işin üç yolu:

```rust
fn main() {
    let list = [10, 20, 30];

    println!("{:?}", list.get(1));
    println!("{:?}", list.get(10));
    println!("{}", list[1]);

    // SAFETY: 1 is smaller than the length 3.
    let value = unsafe { *list.get_unchecked(1) };
    println!("{value}");
}
```

```text
Some(20)
None
20
20
```

| Yazım | Sınır dışında |
|---|---|
| `list.get(10)` | `None` |
| `list[10]` | Panik |
| `list.get_unchecked(10)` | Tanımsız davranış |

Üçüncüyü burada sınır dışında çalıştırmıyoruz: Sonucu söylemek mümkün değil. Tek avantajı sınır denetimini atlamasıdır, ve çoğu programda derleyici o denetimi zaten kaldırır.

## Güvenli soyutlama

`unsafe`'in asıl yeri burası: İçeride `unsafe`, dışarıda güvenli işlev. Bir dilimi iki `&mut` parçaya bölmek isteyelim. Güvenli kodla yazılamaz:

```rust
fn split_pair(list: &mut [i32], mid: usize) -> (&mut [i32], &mut [i32]) {
    let len = list.len();
    (&mut list[..mid], &mut list[mid..len])
}

fn main() {
    let mut list = [1, 2];
    split_pair(&mut list, 1);
}
```

```text
error[E0499]: cannot borrow `*list` as mutable more than once at a time
 --> main.rs:3:29
  |
1 | fn split_pair(list: &mut [i32], mid: usize) -> (&mut [i32], &mut [i32]) {
  |                     - let's call the lifetime of this reference `'1`
2 |     let len = list.len();
3 |     (&mut list[..mid], &mut list[mid..len])
  |     ------------------------^^^^-----------
  |     |     |                 |
  |     |     |                 second mutable borrow occurs here
  |     |     first mutable borrow occurs here
  |     returning this value requires that `*list` is borrowed for `'1`
  |
  = help: use `.split_at_mut(position)` to obtain two mutable non-overlapping sub-slices
```

Derleyici iki parçanın çakışmadığını bilmiyor. Biz biliyoruz:

```rust
use std::slice;

fn split_pair(list: &mut [i32], mid: usize) -> (&mut [i32], &mut [i32]) {
    assert!(mid <= list.len());
    let len = list.len();
    let p = list.as_mut_ptr();

    // SAFETY: mid <= len was checked, so both parts are in bounds.
    // The parts do not overlap, so the two &mut do not alias.
    unsafe {
        (
            slice::from_raw_parts_mut(p, mid),
            slice::from_raw_parts_mut(p.add(mid), len - mid),
        )
    }
}

fn main() {
    let mut list = [1, 2, 3, 4];
    let (a, b) = split_pair(&mut list, 1);
    a[0] = 10;
    b[0] = 20;
    println!("{list:?}");
}
```

```text
[10, 20, 3, 4]
```

Üç şeye bak:

1. **Şart önce denetleniyor.** `assert!` sayesinde kötü `mid` panik olur, tanımsız davranış olmaz.
2. **`// SAFETY:` yorumu** neden doğru olduğunu yazıyor. Bu yorum kodun bir parçası gibidir; yazılamıyorsa kod muhtemelen yanlıştır.
3. **İşlev `unsafe` değil.** Çağıran hiçbir girdiyle tanımsız davranış üretemez. İyi bir güvenli soyutlamanın ölçütü budur.

Standart kütüphanenin `split_at_mut`'ı aynen böyle yazılmıştır.

## unsafe fn

Bir şartı işlevin kendisi denetleyemiyorsa, şartı çağırana yüklersin. O zaman işlev `unsafe fn` olur ve belgeye `# Safety` başlığı yazılır:

```rust
/// Returns the first item without checking.
///
/// # Safety
///
/// `list` must not be empty.
unsafe fn first_unchecked(list: &[i32]) -> i32 {
    // SAFETY: the caller guarantees the list is not empty.
    unsafe { *list.get_unchecked(0) }
}

fn first_or_zero(list: &[i32]) -> i32 {
    if list.is_empty() {
        return 0;
    }
    // SAFETY: the empty case returned just above.
    unsafe { first_unchecked(list) }
}

fn main() {
    println!("{}", first_or_zero(&[7, 8]));
    println!("{}", first_or_zero(&[]));
}
```

```text
7
0
```

Rust 2024'te `unsafe fn` gövdesi kendiliğinden `unsafe` sayılmaz, içeride de blok yazılır. Yazılmazsa derleyici uyarır:

```rust
/// # Safety
/// `list` must not be empty.
unsafe fn first_unchecked(list: &[i32]) -> i32 {
    *list.get_unchecked(0)
}

fn main() {
    // SAFETY: the list has an item.
    println!("{}", unsafe { first_unchecked(&[1]) });
}

```

```text
warning[E0133]: call to unsafe function `core::slice::<impl [T]>::get_unchecked` is
unsafe and requires unsafe block
 --> main.rs:4:6
  |
4 |     *list.get_unchecked(0)
  |      ^^^^^^^^^^^^^^^^^^^^^ call to unsafe function
  |
  = note: consult the function's documentation for information on how to avoid undefined
    behavior
note: an unsafe function restricts its caller, but its body is safe by default
 --> main.rs:3:1
  |
3 | unsafe fn first_unchecked(list: &[i32]) -> i32 {
  | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  = note: for more information, see
    <https://doc.rust-lang.org/edition-guide/rust-2024/unsafe-op-in-unsafe-fn.html>
  = note: `#[warn(unsafe_op_in_unsafe_fn)]` (part of `#[warn(rust_2024_compatibility)]`)
    on by default


For more information about this error, try `rustc --explain E0133`.
```

Böylece gövdede hangi satırın tehlikeli olduğu görünür kalır.

## Ne zaman?

| Durum | Karar |
|---|---|
| Güvenli yolu var | `unsafe` yazma |
| Hız için | Önce ölç; çoğu zaman fark yok |
| Temel veri yapısı yazıyorsun | Gerekebilir, küçük tut |
| C kütüphanesi çağırıyorsun | Gerekli (FFI bölümü) |

Bir projede `unsafe` ne kadar azsa, denetlenecek yer o kadar azdır.

## Özet

- `unsafe`: Beş yetki, derleyici yerine sen garanti edersin.
- Ödünç kuralları `unsafe` içinde de çalışır.
- Kural bozulursa tanımsız davranış: Çalışıyor görünmesi kanıt değildir.
- İçeride `unsafe`, dışarıda güvenli işlev; `// SAFETY:` yorumu zorunlu alışkanlık.
- `unsafe fn`: Şartı çağırana yükler, `# Safety` ile belgelenir.
