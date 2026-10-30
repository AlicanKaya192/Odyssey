# Standart Trait'ler ve derive

Rust'ın bildiğin işlerinin çoğu aslında trait'tir: `{:?}` yazdırmak `Debug`, `==` `PartialEq`, `.clone()` `Clone`, `+` `Add`. Yani kendi türüne bu yetenekleri sen verebilirsin. Çoğunu derleyici tek satırla yazar.

## derive

`#[derive(...)]` derleyiciye "bu trait'in kodunu benim yerime üret" der:

```rust
#[derive(Debug, Clone, PartialEq)]
struct Point {
    x: i32,
    y: i32,
}

fn main() {
    let a = Point { x: 1, y: 2 };
    let b = a.clone();
    println!("{:?}", a);
    println!("{}", a == b);
}
```

```text
Point { x: 1, y: 2 }
true
```

| Trait | Ne verir | derive için şart |
|---|---|---|
| `Debug` | `{:?}` | Alanlar `Debug` |
| `Clone` | `.clone()` | Alanlar `Clone` |
| `Copy` | Atamada kopya | Alanlar `Copy`, ayrıca `Clone` |
| `PartialEq` | `==`, `!=` | Alanlar `PartialEq` |
| `Eq` | Tam eşitlik garantisi | `PartialEq`, ondalık yok |
| `PartialOrd` | `<`, `>` | `PartialEq` |
| `Ord` | Tam sıralama, `.sort()` | `Eq`, `PartialOrd` |
| `Hash` | `HashMap` anahtarı | Alanlar `Hash` |
| `Default` | `T::default()` | Alanlar `Default` |

## Copy ve Clone

`Clone` açıkça kopya alır, `Copy` atamada kendiliğinden olur. `String` barındıran türe `Copy` yazılamaz:

```rust
#[derive(Clone, Copy)]
struct Named {
    name: String,
}

fn main() {
    let a = Named { name: String::from("x") };
    let b = a;
    println!("{}", b.name);
}
```

```text
error[E0204]: the trait `Copy` cannot be implemented for this type
 --> main.rs:2:8
  |
1 | #[derive(Clone, Copy)]
  |                 ---- in this derive macro expansion
2 | struct Named {
  |        ^^^^^
3 |     name: String,
  |     ------------ this field does not implement `Copy`
```

Kural: `Copy` yalnızca bitleri kopyalamanın yeterli olduğu türler içindir. Öbekte verisi olan tür iki kez silinirdi.

## PartialEq ve Eq

`Partial` neden var? `f64` yüzünden: `NaN` kendisine eşit değildir, yani "her değer kendine eşittir" kuralı bozulur.

```rust
fn main() {
    let nan = f64::NAN;
    println!("{}", nan == nan);
    println!("{}", 1.5 == 1.5);
    println!("{}", nan < 1.0);
    println!("{}", nan > 1.0);
}
```

```text
false
true
false
false
```

Bu yüzden `f64` alanlı struct `Eq`, `Ord`, `Hash` alamaz. Sonuç olarak `f64` `HashMap` anahtarı olamaz ve `Vec<f64>` `.sort()` ile sıralanamaz.

## Sıralama

`derive(PartialOrd, Ord)` alanları **yazıldıkları sırayla** karşılaştırır, enum'da seçenekleri yazıldıkları sırayla:

```rust
#[derive(Debug, PartialEq, Eq, PartialOrd, Ord)]
enum Level {
    Low,
    High,
}

#[derive(Debug, PartialEq, Eq, PartialOrd, Ord)]
struct Task {
    level: Level,
    name: String,
}

fn main() {
    println!("{}", Level::Low < Level::High);
    let mut tasks = vec![
        Task { level: Level::High, name: String::from("b") },
        Task { level: Level::Low, name: String::from("z") },
        Task { level: Level::High, name: String::from("a") },
    ];
    tasks.sort();
    for t in &tasks {
        println!("{:?} {}", t.level, t.name);
    }
}
```

```text
true
Low z
High a
High b
```

Başka bir sıra istiyorsan elle yazarsın ya da `sort_by_key`:

```rust
fn main() {
    let mut words = vec!["pear", "fig", "banana"];
    words.sort_by_key(|w| w.len());
    println!("{:?}", words);
    words.sort_by(|a, b| b.cmp(a));
    println!("{:?}", words);
}
```

```text
["fig", "pear", "banana"]
["pear", "fig", "banana"]
```

## Default

```rust
#[derive(Debug, Default)]
struct Settings {
    name: String,
    retries: u32,
    verbose: bool,
    limit: Option<u32>,
}

fn main() {
    println!("{:?}", Settings::default());
    let s = Settings { retries: 3, ..Default::default() };
    println!("{}", s.retries);
}
```

```text
Settings { name: "", retries: 0, verbose: false, limit: None }
3
```

`..Default::default()` "geri kalan alanlar varsayılan olsun" demektir. Sayı `0`, metin boş, `bool` `false`, `Option` `None` olur.

## Display: Elle yazılan

`Debug` geliştirici içindir ve türetilir. `{}` için `Display` kullanıcı içindir, derleyici senin ne yazmak istediğini bilemez, bu yüzden **derive edilmez**:

```rust
use std::fmt;

struct Money {
    cents: u32,
}

impl fmt::Display for Money {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "${}.{:02}", self.cents / 100, self.cents % 100)
    }
}

fn main() {
    let price = Money { cents: 1205 };
    println!("{price}");
    println!("{}", price.to_string().len());
}
```

```text
$12.05
6
```

`write!` `println!` gibidir, ama çıktıyı `f`'ye yazar. `Display` yazınca `.to_string()` bedavaya gelir.

## From ve Into

`From`, bir türden öbürüne dönüşümü tanımlar. Birini yazınca `Into` kendiliğinden gelir:

```rust
#[derive(Debug)]
struct Celsius(f64);

struct Fahrenheit(f64);

impl From<Fahrenheit> for Celsius {
    fn from(f: Fahrenheit) -> Celsius {
        Celsius((f.0 - 32.0) * 5.0 / 9.0)
    }
}

fn main() {
    let a = Celsius::from(Fahrenheit(212.0));
    let b: Celsius = Fahrenheit(32.0).into();
    println!("{:?} {:?}", a, b);
    println!("{:?}", u8::try_from(300).is_err());
}
```

```text
Celsius(100.0) Celsius(0.0)
true
```

`String::from("a")` bu trait'tir. Önceki modülde `.ok_or("metin")?` yazınca `&str`'nin `String`'e dönüşmesini sağlayan da odur: `?` hatayı `From` ile çevirir.

Başarısız olabilen dönüşüm `TryFrom` (`u8::try_from(300)`), metinden okuma `FromStr` (`.parse()` bunu çağırır):

```rust
use std::str::FromStr;

#[derive(Debug)]
struct Point {
    x: i32,
    y: i32,
}

impl FromStr for Point {
    type Err = String;

    fn from_str(text: &str) -> Result<Point, String> {
        let (a, b) = text.split_once(',').ok_or("no comma")?;
        let x = a.parse::<i32>().map_err(|_| "bad x")?;
        let y = b.parse::<i32>().map_err(|_| "bad y")?;
        Ok(Point { x, y })
    }
}

fn main() {
    println!("{:?}", "1,2".parse::<Point>());
    println!("{:?}", "1;2".parse::<Point>());
}
```

```text
Ok(Point { x: 1, y: 2 })
Err("no comma")
```

## İşleçler

`+` aslında `std::ops::Add` trait'idir. Kendi türüne yazabilirsin:

```rust
use std::ops::Add;

#[derive(Debug, Clone, Copy)]
struct Vector {
    x: i32,
    y: i32,
}

impl Add for Vector {
    type Output = Vector;

    fn add(self, other: Vector) -> Vector {
        Vector { x: self.x + other.x, y: self.y + other.y }
    }
}

fn main() {
    let a = Vector { x: 1, y: 2 };
    println!("{:?}", a + a);
}
```

```text
Vector { x: 2, y: 4 }
```

Aynı yolla `Sub`, `Mul`, `Neg`, `Index` da yazılır. Yalnızca gerçekten toplama olan şeye `+` yaz: İşleç sürpriz yapmamalı.

## Özet

- `#[derive]` `Debug`, `Clone`, `Copy`, `PartialEq`, `Eq`, `PartialOrd`, `Ord`, `Hash`, `Default` üretir.
- `Copy` yalnızca öbek verisi olmayan türlerde; `f64` `Eq`, `Ord`, `Hash` alamaz.
- Türetilmiş sıralama alan sırasına bakar.
- `Display` elle yazılır ve `.to_string()` kazandırır.
- `From` dönüşümü tanımlar, `Into` bedavaya gelir, `?` onu kullanır. `FromStr` `.parse()` içindir.
- İşleçler `std::ops` trait'leridir.
