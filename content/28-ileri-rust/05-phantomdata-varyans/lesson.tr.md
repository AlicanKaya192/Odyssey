# PhantomData ve Varyans

Bu bölüm iki soruya cevap veriyor: Alanlarda geçmeyen bir generic parametre nasıl tutulur? Ve `&'static str` neden `&'a str` yerine geçer ama `&mut &'static str` geçmez?

## Kullanılmayan parametre

Rust, struct'ın her generic parametresini alanlarında görmek ister:

```rust
struct Id<T> {
    value: u32,
}

fn main() {}
```

```text
error[E0392]: type parameter `T` is never used
 --> main.rs:1:11
  |
1 | struct Id<T> {
  |           ^ unused type parameter
  |
  = help: consider removing `T`, referring to it in a field, or using a marker such as
    `PhantomData`
  = help: if you intended `T` to be a const parameter, use `const T: /* Type */` instead
```

`PhantomData<T>` "bu türde bir `T` varmış gibi davran" der. Sıfır baytlıktır, çalışma anında yoktur:

```rust
use std::marker::PhantomData;

struct User;
struct Order;

struct Id<T> {
    value: u32,
    _marker: PhantomData<fn() -> T>,
}

impl<T> Id<T> {
    fn new(value: u32) -> Self {
        Id { value, _marker: PhantomData }
    }
}

fn main() {
    let user: Id<User> = Id::new(7);
    let order: Id<Order> = Id::new(7);
    println!("{} {}", user.value, order.value);
    println!("{}", size_of::<Id<User>>());
    println!("{}", size_of::<PhantomData<String>>());
}
```

```text
7 7
4
0
```

`Id<User>` ile `Id<Order>` artık farklı türlerdir; biri ötekinin yerine geçmez. Çalışma anında ikisi de düz `u32`:

```rust
use std::marker::PhantomData;

struct User;
struct Order;

struct Id<T> {
    value: u32,
    _marker: PhantomData<fn() -> T>,
}

fn load_user(id: Id<User>) -> u32 {
    id.value
}

fn main() {
    let order: Id<Order> = Id { value: 7, _marker: PhantomData };
    load_user(order);
}
```

```text
error[E0308]: mismatched types
  --> main.rs:17:15
   |
17 |     load_user(order);
   |     --------- ^^^^^ expected `Id<User>`, found `Id<Order>`
   |     |
   |     arguments to this function are incorrect
   |
   = note: expected struct `Id<User>`
              found struct `Id<Order>`
note: function defined here
  --> main.rs:11:4
   |
11 | fn load_user(id: Id<User>) -> u32 {
   |    ^^^^^^^^^ ------------
```

## Derleyiciye sahipliği söylemek

Ham işaretçinin arkasındaki sahipliği derleyici görmez. `PhantomData` bunu söyler:

| Yazım | Söylediği |
|---|---|
| `PhantomData<T>` | Bir `T`'ye sahibim |
| `PhantomData<&'a T>` | `'a` boyunca bir `T` ödünç aldım |
| `PhantomData<&'a mut T>` | `'a` boyunca değiştirerek ödünç aldım |

İkincisi en sık kullanılandır. Dilim iterator'ü ham işaretçi tutar, ama listeyi ödünç almış gibi davranmalıdır:

```rust
use std::marker::PhantomData;

struct Iter<'a, T> {
    ptr: *const T,
    left: usize,
    _borrow: PhantomData<&'a T>,
}

fn iter_of<T>(list: &[T]) -> Iter<'_, T> {
    Iter { ptr: list.as_ptr(), left: list.len(), _borrow: PhantomData }
}

impl<'a, T> Iterator for Iter<'a, T> {
    type Item = &'a T;

    fn next(&mut self) -> Option<&'a T> {
        if self.left == 0 {
            return None;
        }
        // SAFETY: left items remain from ptr, and the list is borrowed for 'a.
        let item = unsafe { &*self.ptr };
        self.ptr = unsafe { self.ptr.add(1) };
        self.left -= 1;
        Some(item)
    }
}

fn main() {
    let list = vec![1, 2, 3];
    let total: i32 = iter_of(&list).sum();
    println!("{total}");
}
```

```text
6
```

`PhantomData` olmasaydı `'a` hiçbir alanda geçmezdi ve derlenmezdi. Şimdi `Iter` yaşadıkça liste silinemez.

## Varyans: Neden `&'static` kısalır?

Daha uzun yaşayan bir referans, daha kısası yerine verilebilir. Buna **alt türlük** denir: `'static`, `'a`'nın alt türüdür.

```rust
fn longer<'a>(a: &'a str, b: &'a str) -> &'a str {
    if a.len() > b.len() { a } else { b }
}

fn main() {
    let forever: &'static str = "long text";
    let local = String::from("short");
    println!("{}", longer(forever, &local));
}
```

```text
long text
```

Peki bu ne zaman serbest? **Varyans**, sarmalayan türün bu ilişkiyi koruyup korumadığını söyler:

| Tür | `T` için varyans | Anlamı |
|---|---|---|
| `&'a T`, `Box<T>`, `Vec<T>` | Kovaryant | `T` kısalabilir |
| `&'a mut T`, `Cell<T>`, `RefCell<T>` | Değişmez (invariant) | `T` aynen kalmalı |
| `fn(T)` | Kontravaryant | Ters yön |

## Neden `&mut T` değişmez?

Çünkü kısaltmaya izin verseydi, kısa ömürlü bir değeri uzun ömürlü bir yuvaya yazabilirdik:

```rust
fn set<'a>(slot: &mut &'a str, value: &'a str) {
    *slot = value;
}

fn main() {
    let mut s: &'static str = "start";
    {
        let local = String::from("short");
        set(&mut s, &local);
    }
    println!("{s}");
}
```

```text
error[E0597]: `local` does not live long enough
  --> main.rs:9:21
   |
 6 |     let mut s: &'static str = "start";
   |                ------------ type annotation requires that `local` is borrowed for
   `'static`
 7 |     {
 8 |         let local = String::from("short");
   |             ----- binding `local` declared here
 9 |         set(&mut s, &local);
   |                     ^^^^^^ borrowed value does not live long enough
10 |     }
   |     - `local` dropped here while still borrowed
```

`s`, `'static` söz veriyor. `set` onu `&'a str` gibi görseydi içine kısa ömürlü metni yazardı. Değişmezlik tam bu hatayı önler. Okuma yönündeki `&T`'de böyle bir tehlike yok, o yüzden kovaryant.

## Kendi türünde varyans

Varyansı alanlar belirler. `*mut T` değişmez, `*const T` ve `NonNull<T>` kovaryanttır. Önceki bölümde `MyVec`'te `NonNull` seçmemizin bir sebebi de bu:

```rust
use std::ptr::NonNull;

struct MyVec<T> {
    ptr: NonNull<T>,
    len: usize,
}

fn shorten<'a>(list: MyVec<&'static str>) -> MyVec<&'a str> {
    list
}
```

`*mut T` ile aynı işlev derlenmez:

```rust
struct MyVec<T> {
    ptr: *mut T,
    len: usize,
}

fn shorten<'a>(list: MyVec<&'static str>) -> MyVec<&'a str> {
    list
}

fn main() {}
```

```text
error: lifetime may not live long enough
 --> main.rs:7:5
  |
6 | fn shorten<'a>(list: MyVec<&'static str>) -> MyVec<&'a str> {
  |            -- lifetime `'a` defined here
7 |     list
  |     ^^^^ returning this value requires that `'a` must outlive `'static`
  |
  = note: requirement occurs because of the type `MyVec<&str>`, which makes the generic
    argument `&str` invariant
  = note: the struct `MyVec<T>` is invariant over the parameter `T`
  = help: see <https://doc.rust-lang.org/nomicon/subtyping.html> for more information
    about variance
```

Bir `Vec<&'static str>`, `Vec<&'a str>` yerine geçebilmelidir: Standart `Vec`'te böyledir, bizimkinde de öyle olmalı. `NonNull` kovaryant verir, ama içindeki değeri değiştirdiğimiz için `&mut self` ile korunmasını `unsafe`'te sağlarız.

## PhantomData seçmek

| İstek | Yazım |
|---|---|
| `T`'ye sahibim | `PhantomData<T>` |
| `'a` boyunca ödünç aldım | `PhantomData<&'a T>` |
| Sahip değilim, yalnızca etiket | `PhantomData<fn() -> T>` |
| Değişmez olsun | `PhantomData<Cell<T>>` |

Üçüncüsü `Id<T>` gibi etiketler için en doğrusudur: `T` `Send` olmasa bile etiket kollar arasında geçebilir.

## Özet

- `PhantomData<T>` sıfır bayt; generic parametreye alan gibi davranır.
- Aynı bit, farklı tür: `Id<User>` ve `Id<Order>`.
- `&'a T` kovaryant, `&'a mut T` değişmez. Değişmezlik sallanan referansı önler.
- `NonNull` kovaryant, `*mut T` değişmez.
- `PhantomData<&'a T>`, ham işaretçiye ömür bağlar.
