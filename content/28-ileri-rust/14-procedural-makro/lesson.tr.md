# Procedural Makrolar

`#[derive(Debug)]` yazdığında derleyici yapının alanlarına bakıp kod üretiyor. `macro_rules!` bunu yapamaz: Kalıba uyan parçayı yerine koyar, ama "kaç alan var, adları ne?" diye rastgele kodla inceleyemez. Bunun için **procedural makro** var.

Procedural makro, derleme zamanında çalışan sıradan bir Rust fonksiyonudur. Token alır, token verir. Araya istediğin kodu yazarsın.

## Ayrı bir crate

Derleyici makronun kodunu **çalıştıracağı** için onu önce derleyip kendine yüklemek zorunda. Bu yüzden procedural makrolar kendi crate'inde durur. Kök paket:

```toml
[package]
name = "app"
version = "0.1.0"
edition = "2024"

[dependencies]
my_macros = { path = "my_macros" }
```

`my_macros/Cargo.toml`:

```toml
[package]
name = "my_macros"
version = "0.1.0"
edition = "2024"

[lib]
proc-macro = true
```

`proc-macro = true` bu crate'in türünü belirler.

## İlk makro

Üç tür procedural makro var. En basiti fonksiyon benzeri olandır. `my_macros/src/lib.rs`:

```rust
use proc_macro::TokenStream;

#[proc_macro]
pub fn answer(_input: TokenStream) -> TokenStream {
    "42".parse().unwrap()
}
```

`src/main.rs`:

```rust
use my_macros::answer;

fn main() {
    println!("{}", answer!());
}
```

```text
42
```

`proc_macro` crate'i derleyiciyle gelir, indirilmez. Metni `parse` ile token'a çevirmek en kolay üretim yoludur.

## TokenStream

Girdi metin değil, token dizisidir. Her biri dört türden biridir:

```rust
use proc_macro::{TokenStream, TokenTree};

#[proc_macro]
pub fn token_kinds(input: TokenStream) -> TokenStream {
    let kinds: Vec<&str> = input
        .into_iter()
        .map(|token| match token {
            TokenTree::Ident(_) => "ident",
            TokenTree::Punct(_) => "punct",
            TokenTree::Literal(_) => "literal",
            TokenTree::Group(_) => "group",
        })
        .collect();
    format!("{:?}", kinds.join(" ")).parse().unwrap()
}
```

```rust
use my_macros::token_kinds;

fn main() {
    println!("{}", token_kinds!(total + 1 * (a - b)));
}
```

```text
ident punct literal punct group
```

| Tür | Örnek |
|---|---|
| `Ident` | `total`, `struct` |
| `Punct` | `+`, `:` (tek karakter) |
| `Literal` | `1`, `"text"` |
| `Group` | `(a - b)` bütünüyle; içi `group.stream()` |

Dikkat: Bu bir söz dizimi ağacı değildir. Makro `total`'ın tanımlı olup olmadığını bilmez, `1 * (a - b)`'nin önceliğini de bilmez; yalnızca sıralı token'lar görür. `total` kodda hiç tanımlı değil ve derleme yine geçti, çünkü makro onu yedi.

## Hijyen yok

`macro_rules!` bölümünde makronun tanımladığı değişken dışarıdan görünmüyordu. `parse` ile üretilen kodda ise görünür:

```rust
use proc_macro::TokenStream;

#[proc_macro]
pub fn make_x(_input: TokenStream) -> TokenStream {
    "let x = 1;".parse().unwrap()
}
```

```rust
use my_macros::make_x;

fn main() {
    make_x!();
    println!("{x}");
}
```

```text
1
```

Üretilen adlar çağıranın adlarıyla aynı yerde yaşar. Yani yanlışlıkla çağıranın değişkenini gölgelemek senin elinde. Yardımcı değişkenlere nadir adlar ver (`__macro_temp` gibi).

## derive

`derive` makrosu yapının token'larını alır ve **yanına** kod ekler; yapının kendisini değiştirmez. Kendi `FieldNames`'imizi yazalım: Alan adlarını listelesin.

```rust
use proc_macro::{Delimiter, Spacing, TokenStream, TokenTree};

#[proc_macro_derive(FieldNames)]
pub fn field_names(input: TokenStream) -> TokenStream {
    let tokens: Vec<TokenTree> = input.into_iter().collect();
    let name = struct_name(&tokens);
    let fields = field_list(&tokens);
    format!(
        "impl {name} {{
            fn field_names() -> Vec<&'static str> {{
                vec!{fields:?}
            }}
        }}"
    )
    .parse()
    .unwrap()
}

fn struct_name(tokens: &[TokenTree]) -> String {
    let mut iter = tokens.iter();
    while let Some(token) = iter.next() {
        if token.to_string() == "struct" {
            return iter.next().unwrap().to_string();
        }
    }
    panic!("FieldNames works only on structs");
}

fn field_list(tokens: &[TokenTree]) -> Vec<String> {
    let body = tokens.iter().find_map(|token| match token {
        TokenTree::Group(group) if group.delimiter() == Delimiter::Brace => Some(group),
        _ => None,
    });
    let inner: Vec<TokenTree> = body.unwrap().stream().into_iter().collect();
    // A field name is an identifier directly before a single ':'.
    inner
        .windows(2)
        .filter_map(|pair| match pair {
            [TokenTree::Ident(name), TokenTree::Punct(mark)]
                if mark.as_char() == ':' && mark.spacing() == Spacing::Alone =>
            {
                Some(name.to_string())
            }
            _ => None,
        })
        .collect()
}
```

```rust
use my_macros::FieldNames;

#[derive(FieldNames)]
struct Point {
    x: i32,
    y: i32,
    label: std::string::String,
}

fn main() {
    println!("{:?}", Point::field_names());
    let point = Point { x: 1, y: 2, label: String::new() };
    println!("{} {} {:?}", point.x, point.y, point.label);
}
```

```text
["x", "y", "label"]
1 2 ""
```

Yapı ayrıştırma elimizde:

- `struct_name`: `struct` kelimesinden sonraki token ad.
- `field_list`: Süslü parantezli grubun içinde, tek `:`'den hemen önceki ad.
- `Spacing::Alone`: `::` iki ayrı `Punct` olarak gelir ve ilkinin `Spacing`'i `Joint`'tir. Bu olmasa `std::string::String`'deki `std` alan sanılırdı.

`format!` içinde üretilecek koddaki süslü parantezler `{{` ve `}}` yazılır.

Bu ayrıştırıcı öğretim için yeterli ama kırılgan: Alan türü `HashMap<K, V>` olsa yine çalışır, ama `enum`, demet yapı ve öznitelikli alanlar için yeniden yazmak gerekir. Birazdan gerçek çözümü konuşacağız.

## attribute

Üçüncü tür öğeyi **değiştirir**: Dönen token'lar özgün öğenin yerine geçer. İki girdisi vardır, argümanlar ve öğenin kendisi:

```rust
use proc_macro::{Delimiter, Group, TokenStream, TokenTree};

#[proc_macro_attribute]
pub fn logged(_args: TokenStream, item: TokenStream) -> TokenStream {
    let mut tokens: Vec<TokenTree> = item.into_iter().collect();

    let mut iter = tokens.iter();
    let mut name = String::new();
    while let Some(token) = iter.next() {
        if token.to_string() == "fn" {
            name = iter.next().unwrap().to_string();
            break;
        }
    }

    let Some(TokenTree::Group(body)) = tokens.pop() else {
        panic!("logged works only on functions");
    };
    let mut new_body: TokenStream =
        format!("println!(\"enter {name}\");").parse().unwrap();
    new_body.extend(body.stream());
    tokens.push(TokenTree::Group(Group::new(Delimiter::Brace, new_body)));
    tokens.into_iter().collect()
}
```

```rust
use my_macros::logged;

#[logged]
fn add(a: i32, b: i32) -> i32 {
    a + b
}

fn main() {
    println!("{}", add(2, 3));
}
```

```text
enter add
5
```

Son token fonksiyonun gövdesi olan süslü parantezli gruptur. Onu çıkardık, başına bir `println!` ekleyip yeni `Group` kurduk, yerine koyduk. Geri koymasaydık fonksiyon gövdesiz kalırdı: Attribute makroda ne geri verirsen kod odur.

## Hata bildirmek

Makro içinde panik derleme hatasına dönüşür:

```rust
use my_macros::FieldNames;

#[derive(FieldNames)]
enum Color {
    Red,
}

fn main() {
    let _ = Color::Red;
}
```

```text
error: proc-macro derive panicked
 --> src/main.rs:3:10
  |
3 | #[derive(FieldNames)]
  |          ^^^^^^^^^^
  |
  = help: message: FieldNames works only on structs

error: could not compile `app` (bin "app") due to 1 previous error
```

Çalışıyor ama "makro patladı" der. Daha düzgünü `compile_error!` üretmektir:

```rust
use proc_macro::TokenStream;

#[proc_macro]
pub fn only_empty(input: TokenStream) -> TokenStream {
    if input.is_empty() {
        return "0".parse().unwrap();
    }
    "compile_error!(\"only_empty takes no arguments\")".parse().unwrap()
}
```

```rust
use my_macros::only_empty;

fn main() {
    println!("{}", only_empty!(1));
}
```

```text
error: only_empty takes no arguments
 --> src/main.rs:4:20
  |
4 |     println!("{}", only_empty!(1));
  |                    ^^^^^^^^^^^^^^
  |
  = note: this error originates in the macro `only_empty` (in Nightly builds, run with
    -Z macro-backtrace for more info)

error: could not compile `app` (bin "app") due to 1 previous error
```

## Özet

- Procedural makro: Derlemede çalışan, `TokenStream` alıp `TokenStream` veren fonksiyon.
- Ayrı crate ve `proc-macro = true` gerekir.
- Üç tür: `#[proc_macro]`, `#[proc_macro_derive]`, `#[proc_macro_attribute]`.
- Token'lar dört türdür; söz dizimi ağacı değildir, tür bilgisi yoktur.
- `derive` yanına ekler, attribute yerine geçer.
- Hata için `compile_error!` üret.
