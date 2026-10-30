## Şablon

Kopyalayıp doldur:

```rust
use std::error::Error;
use std::fmt;
use std::num::ParseIntError;

#[derive(Debug)]
pub enum MyError {
    Parse(ParseIntError),
    Missing(String),
}

impl fmt::Display for MyError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            MyError::Parse(_) => write!(f, "bad number"),
            MyError::Missing(name) => write!(f, "{name} is missing"),
        }
    }
}

impl Error for MyError {
    fn source(&self) -> Option<&(dyn Error + 'static)> {
        match self {
            MyError::Parse(e) => Some(e),
            MyError::Missing(_) => None,
        }
    }
}

impl From<ParseIntError> for MyError {
    fn from(e: ParseIntError) -> Self {
        MyError::Parse(e)
    }
}

fn main() {
    let e = MyError::from("x".parse::<i32>().unwrap_err());
    println!("{e} / {}", e.source().is_some());
    println!("{}", MyError::Missing(String::from("port")));
}
```

## Metin yazarken

| Yap | Yapma |
|---|---|
| `cannot read port` | `Error: cannot read port!` |
| Küçük harfle, noktasız | Baş harf büyük, sonda nokta |
| Girdiyi yaz: `age 200 is too big` | `invalid input` |
| Sebebi `source`'a koy | Sebebi metne de yaz |

Küçük harf ve noktasız yazılır, çünkü metin başka bir cümlenin arkasına eklenebilir: `error: cannot read port`.

## Gözden geçirme soruları

| Soru | Cevap hayırsa |
|---|---|
| Çağıran bu hataya göre başka bir şey yapar mı? | Ayrı durum açma, birleştir |
| Metin neyin yanlış olduğunu söylüyor mu? | Girdiyi ekle |
| Sebep kaybolmadan taşınıyor mu? | `source` ekle |
| Beklenen durum mu, program hatası mı? | Program hatası `panic!` olur |

## Dışa açık enum

Kütüphanede yeni hata eklemek, çağıranın `match`'ini bozar. `#[non_exhaustive]` bunu önler:

```rust
#[non_exhaustive]
pub enum ParseError {
    Empty,
    TooLong,
}
```

Crate dışındaki `match` artık `_` kolu yazmak zorunda; yeni durum eklemek kimseyi bozmaz.
