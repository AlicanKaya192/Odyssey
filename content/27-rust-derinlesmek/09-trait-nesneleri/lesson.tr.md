# Trait Nesneleri: dyn

Generic kod derlemede her tür için ayrı kopya üretir. Peki aynı listede **farklı türler** tutmak istersen? Bir çizim programında daireler ve kareler, hepsi aynı `Vec`'te. Generic bunu yapamaz, çünkü `Vec<T>` tek bir `T` ister. Çözüm **trait nesnesi**: `dyn Trait`.

## Sorun

```rust
trait Shape {
    fn area(&self) -> f64;
    fn name(&self) -> String;
}

struct Circle {
    r: f64,
}

struct Square {
    side: f64,
}

impl Shape for Circle {
    fn area(&self) -> f64 {
        3.0 * self.r * self.r
    }

    fn name(&self) -> String {
        String::from("circle")
    }
}

impl Shape for Square {
    fn area(&self) -> f64 {
        self.side * self.side
    }

    fn name(&self) -> String {
        String::from("square")
    }
}

fn main() {
    let shapes = vec![Circle { r: 1.0 }, Square { side: 2.0 }];
    println!("{}", shapes.len());
}
```

```text
error[E0308]: mismatched types
  --> main.rs:35:42
   |
35 |     let shapes = vec![Circle { r: 1.0 }, Square { side: 2.0 }];
   |                                          ^^^^^^^^^^^^^^^^^^^^ expected `Circle`,
   found `Square`
```

`Vec` tek tür ister ve iki farklı struct var.

## Box<dyn Trait>

`dyn Shape` "`Shape` sağlayan herhangi bir tür" demektir. Boyutu bilinmediği için bir işaretçinin arkasında durur:

```rust
trait Shape {
    fn area(&self) -> f64;
    fn name(&self) -> String;
}

struct Circle {
    r: f64,
}

struct Square {
    side: f64,
}

impl Shape for Circle {
    fn area(&self) -> f64 {
        3.0 * self.r * self.r
    }

    fn name(&self) -> String {
        String::from("circle")
    }
}

impl Shape for Square {
    fn area(&self) -> f64 {
        self.side * self.side
    }

    fn name(&self) -> String {
        String::from("square")
    }
}

fn main() {
    let shapes: Vec<Box<dyn Shape>> = vec![
        Box::new(Circle { r: 1.0 }),
        Box::new(Square { side: 2.0 }),
    ];
    for s in &shapes {
        println!("{} {}", s.name(), s.area());
    }
}
```

```text
circle 3
square 4
```

Her eleman kendi türünün `area`'sını çağırdı. Hangisinin çağrılacağı **çalışma anında** belirlendi.

## Nasıl çalışıyor?

`&dyn Shape` ve `Box<dyn Shape>` iki adres tutar: **Değere** ve **metot tablosuna** (vtable). Çağrı, tablodan fonksiyonu bulup çalıştırır.

Ölçelim:

```rust
trait Shape {
    fn area(&self) -> f64;
    fn name(&self) -> String;
}

struct Circle {
    r: f64,
}

struct Square {
    side: f64,
}

impl Shape for Circle {
    fn area(&self) -> f64 {
        3.0 * self.r * self.r
    }

    fn name(&self) -> String {
        String::from("circle")
    }
}

impl Shape for Square {
    fn area(&self) -> f64 {
        self.side * self.side
    }

    fn name(&self) -> String {
        String::from("square")
    }
}

use std::mem::size_of;

fn main() {
    println!("{}", size_of::<Box<Circle>>());
    println!("{}", size_of::<Box<dyn Shape>>());
    println!("{}", size_of::<&dyn Shape>());
    println!("{}", size_of::<&str>());
}
```

```text
8
16
16
16
```

`Box<Circle>` 8 bayt, `Box<dyn Shape>` 16 bayt: İkinci adres tablo içindir. Buna **şişman işaretçi** (fat pointer) denir. `&str` de böyledir: Adres ve uzunluk.

## Statik mi, dinamik mi?

| | Generic (`impl Trait`) | `dyn Trait` |
|---|---|---|
| Çağrı kararı | Derlemede | Çalışma anında |
| Hız | Satır içine alınabilir | Tablodan bir adım |
| Kod boyutu | Her tür için kopya | Tek kopya |
| Tek listede farklı türler | **Olmaz** | **Olur** |

Varsayılan seçim generic olsun. `dyn`'i farklı türleri bir arada tutman ya da derleme süresini kısaltman gerekince seç. Fark çoğu programda ölçülemeyecek kadar küçüktür.

## Referansla da olur

Sahiplik gerekmiyorsa `&dyn Trait` yeter:

```rust
trait Shape {
    fn area(&self) -> f64;
    fn name(&self) -> String;
}

struct Circle {
    r: f64,
}

struct Square {
    side: f64,
}

impl Shape for Circle {
    fn area(&self) -> f64 {
        3.0 * self.r * self.r
    }

    fn name(&self) -> String {
        String::from("circle")
    }
}

impl Shape for Square {
    fn area(&self) -> f64 {
        self.side * self.side
    }

    fn name(&self) -> String {
        String::from("square")
    }
}

fn describe(shape: &dyn Shape) -> String {
    format!("{} of area {}", shape.name(), shape.area())
}

fn main() {
    println!("{}", describe(&Circle { r: 2.0 }));
    println!("{}", describe(&Square { side: 3.0 }));
}
```

```text
circle of area 12
square of area 9
```

## Her trait nesne olamaz

Trait'in "nesne güvenli" olması gerekir (dyn compatible). Derleyici çağrıyı tablodan yapacağı için metotlar somut türü bilmeden çalışabilmeli:

```rust
trait Copyable {
    fn duplicate(&self) -> Self;
}

struct Item;

impl Copyable for Item {
    fn duplicate(&self) -> Self {
        Item
    }
}

fn main() {
    let _list: Vec<Box<dyn Copyable>> = vec![Box::new(Item)];
}
```

```text
error[E0038]: the trait `Copyable` is not dyn compatible
  --> main.rs:14:28
   |
14 |     let _list: Vec<Box<dyn Copyable>> = vec![Box::new(Item)];
   |                            ^^^^^^^^ `Copyable` is not dyn compatible
   |
note: for a trait to be dyn compatible it needs to allow building a vtable
      for more information, visit
      <https://doc.rust-lang.org/reference/items/traits.html#dyn-compatibility>
  --> main.rs:2:28
   |
 1 | trait Copyable {
   |       -------- this trait is not dyn compatible...
 2 |     fn duplicate(&self) -> Self;
   |                            ^^^^ ...because method `duplicate` references the `Self`
   type in its return type
   = help: consider moving `duplicate` to another trait
   = help: only type `Item` implements `Copyable`; consider using it directly instead.
```

| Engel | Sebep |
|---|---|
| `-> Self` döndürmek | Boyut bilinmiyor |
| Generic metot | Tablo sonsuz büyürdü |
| `self` olmayan fonksiyon | Hangi türün olduğu belli değil |

Çözüm kalıbı: `where Self: Sized` yazmak o metodu trait nesnesinin dışında bırakır.

## Asıl türe dönmek

`dyn` türü unutur. Tür gerçekten geri lazımsa önce trait'e bir yol eklenir ya da `std::any::Any` kullanılır:

```rust
use std::any::Any;

fn describe(value: &dyn Any) -> String {
    if let Some(n) = value.downcast_ref::<i32>() {
        return format!("number {n}");
    }
    if let Some(s) = value.downcast_ref::<String>() {
        return format!("text {s}");
    }
    String::from("unknown")
}

fn main() {
    println!("{}", describe(&5));
    println!("{}", describe(&String::from("hi")));
    println!("{}", describe(&1.5));
}
```

```text
number 5
text hi
unknown
```

Sık `Any` kullanmak tasarım sorununa işaret eder; enum daha doğru olabilir.

## Enum mı, dyn mi?

Aynı işi enum da yapabilir:

```rust
enum Shape {
    Circle(f64),
    Square(f64),
}

impl Shape {
    fn area(&self) -> f64 {
        match self {
            Shape::Circle(r) => 3.0 * r * r,
            Shape::Square(s) => s * s,
        }
    }
}

fn main() {
    let shapes = vec![Shape::Circle(1.0), Shape::Square(2.0)];
    let total: f64 = shapes.iter().map(|s| s.area()).sum();
    println!("{total}");
}
```

```text
7
```

| Soru | Seçim |
|---|---|
| Seçenekler sabit, hepsi senin elinde | `enum` |
| Başkası yeni tür ekleyecek | `dyn` |
| Yeni işlem sık ekleniyor | `enum` |
| Yeni tür sık ekleniyor | `dyn` |

Enum ayrıca öbek ayırmaz.

## Özet

- `dyn Trait` çalışma anında çözülür; `Box<dyn T>` ya da `&dyn T` arkasında durur.
- Şişman işaretçi: Değer adresi ve metot tablosu, 16 bayt.
- Farklı türleri tek listede tutar. Varsayılan yine generic.
- `-> Self`, generic metot ve `self`siz fonksiyon nesne olmayı engeller.
- Sabit seçenekler için enum daha iyidir.
