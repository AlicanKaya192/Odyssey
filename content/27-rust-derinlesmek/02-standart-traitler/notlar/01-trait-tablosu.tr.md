## Hangi tür ne sağlıyor? (ölçüldü)

```rust
use std::hash::Hash;

fn needs_copy<T: Copy>() {}
fn needs_eq<T: Eq>() {}
fn needs_ord<T: Ord>() {}
fn needs_hash<T: Hash>() {}

fn main() {
    needs_copy::<f64>();
    needs_eq::<String>();
    needs_ord::<char>();
    needs_hash::<Vec<String>>();
    println!("all compiled");
}
```

```text
all compiled
```

Fonksiyon gövdesi boş: Derlendiği için kısıtın sağlandığını biliyoruz.

| Tür | `Copy` | `Eq` | `Ord` | `Hash` |
|---|---|---|---|---|
| `i32`, `char`, `bool` | Evet | Evet | Evet | Evet |
| `f64` | Evet | Hayır | Hayır | Hayır |
| `String` | Hayır | Evet | Evet | Evet |
| `Vec<T>` | Hayır | `T` varsa | `T` varsa | `T` varsa |

## Dönüşümler

| Yazım | Ne zaman |
|---|---|
| `x as u8` | Sayılar arası, kesebilir |
| `u64::from(x)` | Kayıpsız |
| `u8::try_from(x)` | Sığmayabilir, `Result` |
| `x.into()` | Hedef tür belliyse |
| `"5".parse::<i32>()` | Metinden, `Result` |
| `x.to_string()` | `Display`'den metne |

## Display biçim seçenekleri

`f.pad(metin)` kullanırsan `{:>10}` gibi hizalama seçenekleri kendi türünde de çalışır. `write!` bunları görmezden gelir.
