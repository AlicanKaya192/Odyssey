## Yazımlar

| İş | Yazım |
|---|---|
| Tanımla | `trait T { fn f(&self); }` |
| Varsayılan | `trait T { fn f(&self) { ... } }` |
| Uygula | `impl T for S { fn f(&self) { ... } }` |
| Parametre, kısa | `fn g(x: &impl T)` |
| Parametre, uzun | `fn g<X: T>(x: &X)` |
| Çok kısıt | `fn g<X: T + U>(x: &X)` |
| `where` | `fn g<X>(x: &X) where X: T + U` |
| Döndür | `fn g() -> impl T` |
| Kapsayıcı | `impl<X: U> T for X { ... }` |
| İlişkili tür | `trait T { type Out; }` |
| Üst trait | `trait T: Display { ... }` |
| Trait'in kendi fonksiyonu | `trait T { fn new() -> Self; }` |

## Self ve self

| Yazım | Anlamı |
|---|---|
| `Self` | Uygulayan tür |
| `self` | Değerin kendisi (sahiplik) |
| `&self` | Okuma için ödünç |
| `&mut self` | Değiştirme için ödünç |

## Üst trait

`trait Report: Display` demek: "`Report` isteyen, `Display` da sağlamalı." `Report`'un varsayılan metotları `Display`'i kullanabilir.

```rust
use std::fmt::{self, Display};

trait Report: Display {
    fn report(&self) -> String {
        format!("[report] {self}")
    }
}

struct Score(u32);

impl Display for Score {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{} points", self.0)
    }
}

impl Report for Score {}

fn main() {
    println!("{}", Score(7).report());
}
```

```text
[report] 7 points
```

## Hatalar

| Kod | Anlamı | Çözüm |
|---|---|---|
| `E0046` | Sözleşmede eksik metot | Metodu yaz |
| `E0277` | Tür trait'i sağlamıyor | `impl` yaz ya da `derive` |
| `E0599` | Trait kapsamda değil | `use trait_adi;` |
| `E0117` | Yetim kuralı | Kendi türünle sar |
| `E0308` | `impl Trait` iki tür döndürüyor | `Box<dyn T>` |
