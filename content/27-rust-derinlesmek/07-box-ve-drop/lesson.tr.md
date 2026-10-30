# Box, Deref ve Drop

Değerler varsayılan olarak yığında durur, `String` ve `Vec` içeriklerini öbeğe koyar. **Akıllı işaretçi** (smart pointer), hem bir adres tutan hem de ek yetenek taşıyan türdür. `String` ve `Vec` zaten akıllı işaretçidir. En basiti `Box`.

## Box: Öbeğe koymak

`Box::new(x)` değeri öbeğe koyar, yığında yalnızca adres kalır:

```rust
fn main() {
    let b = Box::new(5);
    println!("{}", b);
    println!("{}", *b + 1);
    let mut c = Box::new(String::from("hi"));
    c.push('!');
    println!("{c} {}", c.len());
}
```

```text
5
6
hi! 3
```

<figure class="fig"><svg viewBox="0 0 640 110" width="640" xmlns="http://www.w3.org/2000/svg"><text class="dim" x="20" y="24" font-size="13" font-weight="600">yığın (stack)</text><text class="dim" x="390" y="24" font-size="13" font-weight="600">öbek (heap)</text><g><rect class="box" x="20" y="44" width="230" height="44" rx="8"/><text class="ink" x="34" y="71" font-size="14" font-weight="600">b</text><text class="dim" x="110" y="71" font-size="12.5">Box</text></g><g><rect class="box" x="390" y="44" width="220" height="44" rx="8"/><text class="ink" x="404" y="71" font-size="14">5</text></g><path class="curve" d="M250 66 C320 66 320 66 382 66"/><polygon class="dot" points="390,66 380,61 380,71"/></svg><figcaption>Yığında yalnızca adres (8 bayt), değer öbekte.</figcaption></figure>

Kullanımı normal değer gibidir. `Box` kapsamdan çıkınca hem kendisi hem öbekteki değer silinir.

## Neden gerekir?

Üç durum var:

| Durum | Örnek |
|---|---|
| Boyutu derleme zamanında bilinmeyen tür | Özyinelemeli tür |
| Büyük veriyi kopyalamadan taşımak | Yalnızca adres taşınır |
| Türünü bilmeden trait nesnesi tutmak | `Box<dyn Trait>` (bölüm 09) |

## Özyinelemeli tür

Kendini içeren bir tür yazalım: Bağlı liste. Her düğüm değer ve sonraki listeyi tutuyor.

```rust
enum List {
    Cons(i32, List),
    Nil,
}

fn main() {
    let _empty = List::Nil;
}
```

```text
error[E0072]: recursive type `List` has infinite size
 --> main.rs:1:1
  |
1 | enum List {
  | ^^^^^^^^^
2 |     Cons(i32, List),
  |               ---- recursive without indirection
  |
help: insert some indirection (e.g., a `Box`, `Rc`, or `&`) to break the cycle
  |
2 |     Cons(i32, Box<List>),
  |               ++++    +
```

Derleyici `List`'in boyutunu hesaplayamıyor: `List` bir `List` içeriyor, o da bir `List`... Sonsuz. Öneriyi kendisi veriyor: `Box`. Adresin boyutu sabit olduğu için döngü kırılır:

```rust
#[derive(Debug)]
enum List {
    Cons(i32, Box<List>),
    Nil,
}

use List::{Cons, Nil};

fn sum(list: &List) -> i32 {
    match list {
        Cons(value, rest) => value + sum(rest),
        Nil => 0,
    }
}

fn main() {
    let list = Cons(1, Box::new(Cons(2, Box::new(Nil))));
    println!("{:?}", list);
    println!("{}", sum(&list));
}
```

```text
Cons(1, Cons(2, Nil))
3
```

<figure class="fig"><svg viewBox="0 0 640 168" width="640" xmlns="http://www.w3.org/2000/svg"><text class="dim" x="20" y="24" font-size="13" font-weight="600">yığın (stack)</text><text class="dim" x="390" y="24" font-size="13" font-weight="600">öbek (heap)</text><g><rect class="box" x="20" y="44" width="230" height="44" rx="8"/><text class="ink" x="34" y="71" font-size="14" font-weight="600">list</text><text class="dim" x="110" y="71" font-size="12.5">Cons(1, Box)</text></g><g><rect class="box" x="390" y="44" width="220" height="44" rx="8"/><text class="ink" x="404" y="71" font-size="14">Cons(2, Box)</text></g><g><rect class="box" x="390" y="102" width="220" height="44" rx="8"/><text class="ink" x="404" y="129" font-size="14">Nil</text></g><path class="curve" d="M250 66 C320 66 320 66 382 66"/><polygon class="dot" points="390,66 380,61 380,71"/></svg><figcaption>Her düğümde değer ve sonraki düğümün adresi: Boyut sabit.</figcaption></figure>

`Nil` listenin sonu. `use List::{Cons, Nil};` seçenekleri kısa yazmak için.

Boyutları ölçelim:

```rust
#[derive(Debug)]
enum List {
    Cons(i32, Box<List>),
    Nil,
}

use List::{Cons, Nil};

use std::mem::size_of;

fn main() {
    println!("{}", size_of::<Box<i32>>());
    println!("{}", size_of::<Box<[i32; 1000]>>());
    println!("{}", size_of::<[i32; 1000]>());
    println!("{}", size_of::<List>());
}
```

```text
8
8
4000
16
```

## Deref: * işleci

`Box` neden referans gibi davranıyor? `Deref` trait'i sayesinde. `*x` aslında `*(x.deref())` demektir:

```rust
use std::ops::Deref;

struct MyBox<T>(T);

impl<T> Deref for MyBox<T> {
    type Target = T;

    fn deref(&self) -> &T {
        &self.0
    }
}

fn main() {
    let x = MyBox(5);
    println!("{}", *x);
    println!("{}", *x.deref());
}
```

```text
5
5
```

`deref` `&T` döndürür. Kendi türüne yazınca `*` onda da çalışır.

## Otomatik dönüşüm

Rust gerektiğinde `deref`'i kendisi zincirler. Bu yüzden `&String` `&str` isteyen yere geçer:

```rust
use std::ops::Deref;

struct MyBox<T>(T);

impl<T> Deref for MyBox<T> {
    type Target = T;

    fn deref(&self) -> &T {
        &self.0
    }
}

fn greet(name: &str) {
    println!("Hello, {name}");
}

fn main() {
    let name = MyBox(String::from("Ada"));
    greet(&name);
    greet(&name.0);
    println!("{}", name.len());
}
```

```text
Hello, Ada
Hello, Ada
3
```

`&MyBox<String>` → `&String` → `&str`. Bu **deref dönüşümü** (deref coercion) çalışma anında maliyetsizdir, derlemede çözülür. Değiştirilebilir sürümü `DerefMut`.

## Drop: Temizlik

`Drop` trait'i "bu değer silinirken şunu çalıştır" der. Dosya kapatmak, kilit bırakmak hep buradadır:

```rust
struct Loud {
    name: &'static str,
}

impl Drop for Loud {
    fn drop(&mut self) {
        println!("dropping {}", self.name);
    }
}

fn main() {
    let _a = Loud { name: "a" };
    let _b = Loud { name: "b" };
    {
        let _inner = Loud { name: "inner" };
        println!("block ends");
    }
    println!("main ends");
}
```

```text
block ends
dropping inner
main ends
dropping b
dropping a
```

**Silinme sırası tanımın tersidir**: Son tanımlanan önce gider. Struct alanları ise yazıldıkları sırayla.

Bu kalıbın adı RAII: Kaynağı değer tutar, değer gidince kaynak da gider. `finally` ya da "kapatmayı unuttum" derdi yoktur.

## Erken silmek

`x.drop()` doğrudan çağrılamaz, çünkü sonunda ikinci kez silinirdi:

```rust
struct Loud {
    name: &'static str,
}

impl Drop for Loud {
    fn drop(&mut self) {
        println!("dropping {}", self.name);
    }
}

fn main() {
    let a = Loud { name: "a" };
    a.drop();
}
```

```text
error[E0040]: explicit use of destructor method
  --> main.rs:13:7
   |
13 |     a.drop();
   |       ^^^^ explicit destructor calls not allowed
   |
help: consider using `drop` function
   |
13 -     a.drop();
13 +     drop(a);
   |
```

Doğrusu `std::mem::drop(x)` (otomatik gelir, `drop(x)`). Kendisi çok basit: Sahipliği alır, hiçbir şey yapmaz, kapsam biter:

```rust
struct Loud {
    name: &'static str,
}

impl Drop for Loud {
    fn drop(&mut self) {
        println!("dropping {}", self.name);
    }
}

fn main() {
    let a = Loud { name: "a" };
    drop(a);
    println!("after drop");
}
```

```text
dropping a
after drop
```

## Özet

- `Box::new(x)` değeri öbeğe koyar, adres sabit boyuttadır.
- Özyinelemeli tür `Box` ister (`E0072`). Büyük veri ve trait nesnesi diğer kullanımlar.
- `Deref` `*`'ı sağlar. Deref dönüşümü `&String`'i `&str`'ye çevirir, bedeli yok.
- `Drop` temizliği yazar. Sıra tanımın tersi. RAII: Kaynak değere bağlı.
- Erken silmek için `drop(x)`; `x.drop()` yasak (`E0040`).
