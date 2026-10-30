# Modüller ve Görünürlük

Program büyüdükçe tek dosya yetmez. **Modül** kodu adlandırılmış bölümlere ayırır ve neyin dışarıdan görüneceğini belirler. Rust'ta her şey varsayılan olarak **gizlidir** (private).

## mod ve pub

```rust
mod shapes {
    pub fn area(w: u32, h: u32) -> u32 {
        w * h
    }

    pub fn perimeter(w: u32, h: u32) -> u32 {
        double(w + h)
    }

    fn double(n: u32) -> u32 {
        n * 2
    }
}

fn main() {
    println!("{}", shapes::area(3, 4));
    println!("{}", shapes::perimeter(3, 4));
}
```

```text
12
14
```

`mod` bir modül açar, `::` içine girer. `pub` "dışarıdan görünsün" demektir.

`pub` unutulursa:

```rust
mod shapes {
    fn area(w: u32, h: u32) -> u32 {
        w * h
    }
}

fn main() {
    println!("{}", shapes::area(3, 4));
}
```

```text
error[E0603]: function `area` is private
 --> main.rs:8:28
  |
8 |     println!("{}", shapes::area(3, 4));
  |                            ^^^^ private function
  |
note: the function `area` is defined here
 --> main.rs:2:5
  |
2 |     fn area(w: u32, h: u32) -> u32 {
  |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```

Bu sınırlama bir özelliktir: `pub` yazmadığın her şeyi, kimseyi bozmadan değiştirebilirsin.

## use: Kısa ad

Tam yolu her seferinde yazmak uzun sürer:

```rust
mod shapes {
    pub mod circle {
        pub fn area_times_100(r: u32) -> u32 {
            314 * r * r
        }
    }
}

use shapes::circle;

fn main() {
    println!("{}", shapes::circle::area_times_100(2));
    println!("{}", circle::area_times_100(1));
}
```

```text
1256
314
```

`use` adı bulunduğu kapsama getirir. Standart kütüphane için zaten yazıyorduk: `use std::collections::HashMap;`. `as` adı değiştirir, süslü parantez birkaçını birden alır:

```rust
use std::collections::{BTreeMap, HashMap};
use std::fmt::Result as FmtResult;
```

Fonksiyonda genelde modülü (`shapes::area`), tür ve struct'ta kendisini (`HashMap`) getirmek gelenektir: Çağrıya bakınca fonksiyonun nereden geldiği belli olur.

## Yollar: crate, self, super

| Yazım | Nereden başlar |
|---|---|
| `crate::a::b` | Projenin kökünden |
| `self::b` | Bulunduğun modülden |
| `super::b` | Bir üst modülden |

```rust
fn top() -> &'static str {
    "top"
}

mod outer {
    pub fn name() -> &'static str {
        "outer"
    }

    pub mod inner {
        pub fn report() {
            println!("{}", super::name());
            println!("{}", self::own());
            println!("{}", crate::top());
        }

        fn own() -> &'static str {
            "inner"
        }
    }
}

fn main() {
    outer::inner::report();
}
```

```text
outer
inner
top
```

Testlerdeki `use super::*;` tam olarak budur: Test modülü üst modüldeki her şeyi içeri alır.

## Struct alanları da gizlidir

`pub struct` yazmak alanları açmaz. Her alan için ayrıca `pub` gerekir:

```rust
mod people {
    pub struct Age {
        value: u8,
    }
}

fn main() {
    let age = people::Age { value: 200 };
    println!("{}", age.value);
}
```

```text
error[E0616]: field `value` of struct `Age` is private
 --> main.rs:9:24
  |
9 |     println!("{}", age.value);
  |                        ^^^^^ private field
```

Önceki bölümün "doğrulayan kurucu" fikri işte burada tamamlanıyor. Alan gizli olduğu için geçersiz değer ancak kurucudan geçerek oluşabilir, o da reddeder:

```rust
mod people {
    #[derive(Debug)]
    pub struct Age {
        value: u8,
    }

    impl Age {
        pub fn new(value: i32) -> Result<Age, String> {
            if value < 0 || value > 150 {
                return Err(format!("age must be 0-150, got {value}"));
            }
            Ok(Age { value: value as u8 })
        }

        pub fn get(&self) -> u8 {
            self.value
        }
    }
}

fn main() {
    let age = people::Age::new(36).expect("valid");
    println!("{}", age.get());
    println!("{:?}", people::Age::new(200));
}
```

```text
36
Err("age must be 0-150, got 200")
```

Enum ise farklıdır: `pub enum`'un bütün seçenekleri açıktır.

## Modül dosyaları

`mod lib_name;` (noktalı virgülle) "bu modülün içeriği başka dosyada" demektir:

```text
src/
├── main.rs        mod shapes;
└── shapes.rs      pub fn area(...)
```

Alt modüller klasörde durur:

```text
src/
├── main.rs        mod shapes;
├── shapes.rs      pub mod circle;
└── shapes/
    └── circle.rs  pub fn area(...)
```

Eski projelerde `shapes/mod.rs` görürsün, aynı işi yapar. Dosyanın içine `mod shapes { ... }` **yazılmaz**, dosyanın kendisi modüldür.

Çalışan bir örnek:

```rust
mod shapes;

fn main() {
    println!("{}", shapes::area(3, 4));
}
```

```text
12
```

`shapes.rs` içeriği:

```rust
pub fn area(w: u32, h: u32) -> u32 {
    w * h
}

```

Rust dosyaları kendiliğinden bulmaz. `mod shapes;` satırı olmayan dosya derlenmez bile. Python'daki "dosya vardır, modüldür" alışkanlığından farklı.

## Paket, crate, modül

| Kavram | Ne |
|---|---|
| **Paket** (package) | `Cargo.toml` olan klasör |
| **Crate** | Derleyicinin tek seferde derlediği birim |
| **İkili crate** | `src/main.rs`: Çalışan program |
| **Kütüphane crate** | `src/lib.rs`: Başkasının kullanacağı kod |
| **Modül** | Crate içindeki bölüm |

Bir paket hem `main.rs` hem `lib.rs` taşıyabilir. İyi bir düzen şudur: Bütün mantık `lib.rs`'te, `main.rs` yalnızca okuyup çağırır. Böylece mantık test edilebilir kalır.

```rust
// src/lib.rs
pub fn greet(name: &str) -> String {
    format!("Hello, {name}!")
}
```

```rust
// src/main.rs (paketin adı hello ise)
fn main() {
    println!("{}", hello::greet("Ada"));
}
```

## pub'un dereceleri

| Yazım | Kim görür |
|---|---|
| (yok) | Bu modül ve altındakiler |
| `pub(super)` | Bir üst modül |
| `pub(crate)` | Bütün crate |
| `pub` | Herkes |

Bir şeyi yalnızca gerektiği kadar aç: `pub` bir kere yazılıp başkası kullanmaya başlayınca geri almak zorlaşır.

## pub use: Yeniden dışa açmak

İç düzen ile dışarıya sunulan yüz farklı olabilir:

```rust
mod geometry {
    mod circle {
        pub fn area_times_100(r: u32) -> u32 {
            314 * r * r
        }
    }

    pub use circle::area_times_100;
}

fn main() {
    println!("{}", geometry::area_times_100(2));
}
```

```text
1256
```

Kullanan kişi `geometry::circle::area` yerine `geometry::area` yazar. İç klasör düzenini değiştirsen de onun kodu bozulmaz.

## Özet

- `mod` modül açar, `::` içine girer; her şey varsayılan gizlidir.
- `pub` açar. Struct'ta her alan ayrıca `pub` ister; enum seçenekleri kendiliğinden açıktır.
- `use` kısa ad getirir. `crate::`, `self::`, `super::` yol başlangıçlarıdır.
- `mod x;` içeriği `x.rs`'ten alır; dosya kendiliğinden bulunmaz.
- `main.rs` ikili, `lib.rs` kütüphane crate'idir. Mantığı kütüphaneye koy.
- `pub use` iç düzenden bağımsız bir yüz sunar.
