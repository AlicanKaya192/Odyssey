# Struct ve Metotlar

Bir kullanıcının adı, yaşı ve e-postası birbirine aittir. Bunları ayrı ayrı değişkenlerde tutmak yerine tek bir türde toplarız. **Struct** (yapı) kendi türünü tanımlamanın yoludur.

## Struct tanımlamak

```rust
struct User {
    name: String,
    age: u32,
}

fn main() {
    let user = User {
        name: String::from("Ada"),
        age: 36,
    };
    println!("{} {}", user.name, user.age);
}
```

```text
Ada 36
```

- `struct` yeni bir tür tanımlar. Tür adları `PascalCase` yazılır.
- Süslü parantezin içindeki `name: String` satırlarına **alan** (field) denir.
- Değer oluştururken bütün alanlar verilmelidir, sıra önemli değildir.
- Alana `.` ile ulaşılır.

Değiştirmek için değişkenin tamamı `mut` olmalıdır. Rust'ta tek bir alanı `mut` yapmak diye bir şey yoktur:

```rust
struct User {
    name: String,
    age: u32,
}

fn main() {
    let mut user = User {
        name: String::from("Ada"),
        age: 36,
    };
    user.age += 1;
    println!("{}", user.age);
}
```

```text
37
```

## Kısa yazımlar

Alan adıyla değişken adı aynıysa bir kez yazmak yeter. `..` ile geri kalan alanlar başka bir değerden alınır:

```rust
struct Point {
    x: i32,
    y: i32,
    z: i32,
}

fn main() {
    let x = 1;
    let y = 2;
    let base = Point { x, y, z: 3 };
    let moved = Point { x: 10, ..base };
    println!("{} {} {}", moved.x, moved.y, moved.z);
    println!("{}", base.x);
}
```

```text
10 2 3
1
```

Dikkat: `..base` alanları taşır. Burada `name` yeni verildi, kalanlar sayı olduğu için `Copy`, yani `base` hâlâ kullanılabilir. `String` alan taşınsaydı `base`'in o alanı kullanılamazdı.

## Sahiplik ve struct

Struct, alanlarına sahiptir. `String` alanı olan bir struct öbek belleğinin de sahibidir ve kapsamdan çıkınca hepsi silinir. Atama yine taşımadır:

```rust
struct User {
    name: String,
    age: u32,
}

fn main() {
    let first = User { name: String::from("Ada"), age: 36 };
    let second = first;
    println!("{} {}", first.age, second.age);
}
```

```text
error[E0382]: borrow of moved value: `first`
 --> main.rs:9:23
  |
7 |     let first = User { name: String::from("Ada"), age: 36 };
  |         ----- move occurs because `first` has type `User`, which does not implement
  the `Copy` trait
8 |     let second = first;
  |                  ----- value moved here
9 |     println!("{} {}", first.age, second.age);
  |                       ^^^^^^^^^ value borrowed here after move
  |
note: if `User` implemented `Clone`, you could clone the value
 --> main.rs:1:1
  |
1 | struct User {
  | ^^^^^^^^^^^ consider implementing `Clone` for this type
...
8 |     let second = first;
  |                  ----- you could clone this value
```

Alanları referans yapmak isteyebilirsin (`name: &str`), ama bu yaşam süresi gerektirir; ikinci modülde. Şimdilik struct'ların verisine sahip olmasını sağla: `&str` yerine `String`.

## Struct yazdırmak: derive

Struct'ı doğrudan yazdırmayı deneyelim:

```rust
struct Rectangle {
    width: u32,
    height: u32,
}

fn main() {
    let rect = Rectangle { width: 3, height: 4 };
    println!("{:?}", rect);
}
```

```text
error[E0277]: `Rectangle` doesn't implement `Debug`
 --> main.rs:8:22
  |
8 |     println!("{:?}", rect);
  |               ----   ^^^^ `Rectangle` cannot be formatted using `{:?}` because it
  doesn't implement `Debug`
  |               |
  |               required by this formatting parameter
  |
  = help: the trait `Debug` is not implemented for `Rectangle`
help: consider annotating `Rectangle` with `#[derive(Debug)]`
  |
1 + #[derive(Debug)]
2 | struct Rectangle {
  |
```

Mesaj hem sorunu hem çözümü söylüyor. `#[derive(Debug)]` satırı derleyiciden bu türü `{:?}` ile yazdırma kodunu üretmesini ister. `{:#?}` okunaklı, çok satırlı biçim verir:

```rust
#[derive(Debug)]
struct Rectangle {
    width: u32,
    height: u32,
}

fn main() {
    let rect = Rectangle { width: 3, height: 4 };
    println!("{:?}", rect);
    println!("{:#?}", rect);
}
```

```text
Rectangle { width: 3, height: 4 }
Rectangle {
    width: 3,
    height: 4,
}
```

`#[...]` yazımına **öznitelik** (attribute) denir. `derive` birçok hazır özelliği tek satırda ekler; ikinci modülde ayrıntılı göreceğiz.

## Metotlar: impl

Veriye ait işlemleri **metot** olarak tanımlarız. Metotlar `impl` bloğuna yazılır ve ilk parametreleri `self`'tir:

```rust
#[derive(Debug)]
struct Rectangle {
    width: u32,
    height: u32,
}

impl Rectangle {
    fn area(&self) -> u32 {
        self.width * self.height
    }

    fn is_square(&self) -> bool {
        self.width == self.height
    }
}

fn main() {
    let rect = Rectangle { width: 3, height: 4 };
    println!("{}", rect.area());
    println!("{}", rect.is_square());
}
```

```text
12
false
```

Üç `self` biçimi, önceki bölümdeki üç parametreyle aynıdır:

| Yazım | Anlamı | Ne zaman |
|---|---|---|
| `&self` | Okumak için ödünç alır | Çoğu metot |
| `&mut self` | Değiştirmek için ödünç alır | Durum değiştiren metot |
| `self` | Sahipliği alır, değer tükenir | Dönüştüren metot |

Örnekle üçü birden:

```rust
struct Book {
    title: String,
    pages: u32,
}

impl Book {
    fn pages(&self) -> u32 {
        self.pages
    }

    fn add_pages(&mut self, count: u32) {
        self.pages += count;
    }

    fn into_title(self) -> String {
        self.title
    }
}

fn main() {
    let mut book = Book { title: String::from("Rust"), pages: 100 };
    book.add_pages(20);
    println!("{}", book.pages());
    let title = book.into_title();
    println!("{title}");
}
```

```text
120
Rust
```

`into_title` çağrısından sonra `book` kullanılamaz: Sahipliği metoda geçti. Rust'ta `into_` ile başlayan metot adı genellikle bunu anlatır.

`rect.area()` yazınca `&` yazmana gerek yok: Rust gereken `&`, `&mut` ya da `*`'ı kendisi ekler. Bu yüzden **otomatik referanslama** sayesinde çağrı hep aynı görünür.

## İlişkili fonksiyonlar: new

`impl` içinde `self` almayan fonksiyona **ilişkili fonksiyon** denir ve `Tur::ad()` ile çağrılır. `String::from` de böyledir. Rust'ta kurucu diye özel bir şey yok; gelenek `new` adlı bir ilişkili fonksiyondur:

```rust
#[derive(Debug)]
struct Rectangle {
    width: u32,
    height: u32,
}

impl Rectangle {
    fn new(width: u32, height: u32) -> Self {
        Self { width, height }
    }

    fn square(side: u32) -> Self {
        Self::new(side, side)
    }
}

fn main() {
    println!("{:?}", Rectangle::new(2, 5));
    println!("{:?}", Rectangle::square(4));
}
```

```text
Rectangle { width: 2, height: 5 }
Rectangle { width: 4, height: 4 }
```

`Self` içinde bulunduğun türün kısa adıdır: Burada `Rectangle`. Bir tür için birden fazla `impl` bloğu yazılabilir.

## Demet struct ve birim struct

Alan adı gerekmiyorsa **demet struct** yazılır. Asıl faydası aynı temsili taşıyan değerleri karıştırmamaktır:

```rust
struct Meters(f64);
struct Feet(f64);

fn main() {
    let height = Meters(1.8);
    let wall = Feet(9.5);
    println!("{} {}", height.0, wall.0);
}
```

```text
1.8 9.5
```

`Meters` ile `Feet`'in ikisi de `f64` ama derleyici için farklı türlerdir. `add(a, b)` yazarken ikisini karıştırırsan derlenmez:

```rust
struct Meters(f64);
struct Feet(f64);

fn add(a: Meters, b: Meters) -> Meters {
    Meters(a.0 + b.0)
}

fn main() {
    let total = add(Meters(1.0), Feet(2.0));
    println!("{}", total.0);
}
```

```text
error[E0308]: mismatched types
 --> main.rs:9:34
  |
9 |     let total = add(Meters(1.0), Feet(2.0));
  |                 ---              ^^^^^^^^^ expected `Meters`, found `Feet`
  |                 |
  |                 arguments to this function are incorrect
  |
note: function defined here
 --> main.rs:4:4
  |
4 | fn add(a: Meters, b: Meters) -> Meters {
  |    ^^^            ---------
```

Buna **yeni tür kalıbı** (newtype) denir ve bir uzay aracının kaybına yol açmış birim hatasının derleme anında yakalanması anlamına gelir. Hiç alanı olmayan `struct Marker;` da yazılabilir (birim struct); trait'lerde işe yarayacak.

## Özet

- `struct` kendi türünü tanımlar; alanlara `.` ile ulaşılır; değişken `mut` ise bütün alanlar değişebilir.
- Struct alanlarına sahiptir; atama taşımadır. Şimdilik alanlarda `String` kullan.
- `#[derive(Debug)]` ve `{:?}`, `{:#?}` yazdırır.
- `impl` içinde metot yazılır: `&self` okur, `&mut self` değiştirir, `self` tüketir.
- `self` almayan `new` gibi fonksiyonlar `Tur::new()` ile çağrılır.
- Demet struct farklı anlamları aynı temsilde karıştırmayı engeller.
