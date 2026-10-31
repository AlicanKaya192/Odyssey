## Parça türleri

| Tür | Yakaladığı | Örnek |
|---|---|---|
| `expr` | İfade | `1 + 2`, `f(x)` |
| `ident` | Ad | `value`, `Point` |
| `ty` | Tür | `i32`, `Vec<u8>` |
| `tt` | Tek token ya da parantezli grup | `+`, `(a b)` |
| `pat` | Desen | `Some(x)`, `1..=5` |
| `stmt` | Deyim | `let a = 1` |
| `block` | Blok | `{ a + 1 }` |
| `literal` | Sabit değer | `3`, `"text"` |
| `path` | Yol | `std::mem::swap` |
| `item` | Öğe | `fn f() {}`, `struct S;` |
| `lifetime` | Ömür | `'a` |
| `vis` | Görünürlük, boş olabilir | `pub`, `pub(crate)` |
| `meta` | Öznitelik içeriği | `derive(Debug)` |

## Tekrar kalıpları

| Kalıp | Uyan |
|---|---|
| `$( $x:expr ),*` | `a, b, c` ya da hiçbir şey |
| `$( $x:expr ),+` | En az bir |
| `$( $x:expr ),* $(,)?` | Sonda virgül de olabilir |
| `$( $x:tt )*` | Boşlukla ayrılmış token'lar |
| `$( $k:expr => $v:expr ),*` | Çiftler |

Şablonda tekrar, kalıptakiyle aynı derinlikte olmalıdır: `$x` tekrar içinde yakalandıysa `$( ... $x ... )*` içinde kullanılır.

## Sık kullanılan yerleşik makrolar

| Makro | Verdiği |
|---|---|
| `stringify!(x)` | Token'ların metni |
| `concat!("a", 1)` | Birleşik sabit metin |
| `line!()`, `column!()`, `file!()` | Kaynaktaki yer |
| `module_path!()` | Modül yolu |
| `env!("AD")` | Derleme anındaki ortam değişkeni |
| `include_str!("yol")` | Dosyayı metin olarak gömer |
| `compile_error!("mesaj")` | Derlemeyi mesajla durdurur |
| `cfg!(windows)` | Yapılandırma koşulu, `bool` |

## Çağrı biçimleri

`m!()`, `m![]`, `m!{}` üçü de geçerlidir ve aynı kollara gider. Alışkanlık: fonksiyon gibi olanlar `()`, liste gibi olanlar `[]`, öğe üretenler `{}` ya da sonunda `;` ile `()`.

## Modül ve crate

| İhtiyaç | Yazım |
|---|---|
| Aynı dosyada, aşağıda | Doğrudan kullan |
| Crate içinde yolla | `pub(crate) use ad;` |
| Başka crate'lere | `#[macro_export]` |
| Makro içinde kendi crate'in | `$crate::yol` |
