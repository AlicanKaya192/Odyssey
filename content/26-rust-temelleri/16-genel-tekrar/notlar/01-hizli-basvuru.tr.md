## Yazımlar

| İş | Yazım |
|---|---|
| Değişmez, değişir | `let x = 1;`, `let mut x = 1;` |
| Sabit | `const MAX: u32 = 10;` |
| Fonksiyon | `fn add(a: i32, b: i32) -> i32 { a + b }` |
| Koşul | `if a > 0 { .. } else { .. }` |
| Döngüler | `loop`, `while k`, `for x in 0..3` |
| Struct | `struct P { x: i32 }`, `impl P { fn f(&self) {} }` |
| Enum | `enum E { A, B(i32) }` |
| Desen | `match v { E::A => .., E::B(n) => .. }` |
| Tek desen | `if let Some(x) = v { .. }` |
| Liste | `vec![1, 2]`, `v.push(3)`, `v.get(0)` |
| Harita | `HashMap::new()`, `m.insert(k, v)`, `m.entry(k).or_insert(0)` |
| Metin | `String::from("a")`, `&s[0..1]`, `s.len()` |
| Hata | `Ok(v)`, `Err(e)`, `f()?` |
| Modül | `mod a;`, `pub fn`, `use a::b;` |
| Test | `#[test]`, `assert_eq!(a, b)` |

## Sahiplik kuralları

1. Her değerin bir sahibi var.
2. Aynı anda yalnızca bir sahip.
3. Sahip kapsamdan çıkınca değer silinir.

## Ödünç alma kuralları

1. Aynı anda ya birçok `&T` ya da tek `&mut T`.
2. Referans her zaman geçerli olmalı.

## Sık görülen hatalar

| Kod | Anlamı | Genelde çözüm |
|---|---|---|
| `E0382` | Taşınmış değer kullanıldı | Ödünç al ya da `clone` |
| `E0499` | İki `&mut` | Birini bitir |
| `E0502` | `&` varken `&mut` | Kapsamı daralt |
| `E0505` | Ödünçlüyken taşındı | Sırayı değiştir |
| `E0384` | `mut` olmayana iki kez atama | `mut` ekle |
| `E0596` | `mut` olmayandan `&mut` | `mut` ekle |
| `E0308` | Tür uyuşmuyor | Türü düzelt |
| `E0004` | `match` eksik dal | Dalı ekle |
| `E0106` | Ömür eksik | Sahipli değer döndür |
| `E0277` | Özellik eksik | Hata metnine bak |
| `E0603` | Gizli ad | `pub` ekle |

## Cargo

| Komut | İş |
|---|---|
| `cargo new ad` | Yeni proje |
| `cargo run` | Derle ve çalıştır |
| `cargo check` | Yalnızca denetle |
| `cargo test` | Testler |
| `cargo build --release` | En iyileştirilmiş derleme |
| `cargo fmt`, `cargo clippy` | Biçim, öneriler |
