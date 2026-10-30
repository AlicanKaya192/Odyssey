## Yetim kuralını aşmak: Sarmalayıcı

Başkasının trait'ini başkasının türüne yazamazsın, ama türü kendi türünle sarabilirsin. Bunun adı **yeni tür** (newtype) kalıbıdır:

```rust
use std::fmt::{self, Display};

struct Words(Vec<String>);

impl Display for Words {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "[{}]", self.0.join(", "))
    }
}

fn main() {
    let w = Words(vec![String::from("a"), String::from("b")]);
    println!("{w}");
}
```

```text
[a, b]
```

Tek alanlı struct'ın çalışma anı bedeli yoktur.

## Trait mi, enum mu?

| Soru | Seçim |
|---|---|
| Seçenekler sabit ve senin elinde | `enum` |
| Başkası yeni tür ekleyebilmeli | `trait` |
| `match` ile her seçenek ele alınmalı | `enum` |
| Her tür kendi davranışını yazsın | `trait` |

## Trait neden kapsamda olmalı?

Bir trait'in metodunu çağırmak için trait'in `use` ile içeri alınmış olması gerekir. `std::fmt::Write` ile `std::io::Write` gibi aynı adlı metotları olan trait'ler böylece karışmaz. Hata metni çoğu zaman hangi `use` gerektiğini söyler.

## Küçük tut

Tek işi anlatan küçük trait'ler daha çok yerde kullanılır. Standart kütüphane örnekleri: `Display` tek metot, `Clone` iki, `Iterator` bir zorunlu metot ve onlarca varsayılan.

## Aynı adlı metotlar

İki trait aynı adı taşıyorsa hangisi kastedildiği yazılır:

```rust
Pilot::fly(&person);
Wizard::fly(&person);
```

Tam yazım gerekirse: `<Human as Pilot>::fly(&person)`.
