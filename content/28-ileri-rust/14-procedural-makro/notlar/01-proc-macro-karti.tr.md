## Üç tür

| Tür | Öznitelik | İmza | Çağrı |
|---|---|---|---|
| Fonksiyon benzeri | `#[proc_macro]` | `fn(TokenStream) -> TokenStream` | `name!(...)` |
| Derive | `#[proc_macro_derive(Name)]` | `fn(TokenStream) -> TokenStream` | `#[derive(Name)]` |
| Attribute | `#[proc_macro_attribute]` | `fn(TokenStream, TokenStream) -> TokenStream` | `#[name(...)]` |

## Ne ne yapar?

| Tür | Girdi | Çıktı |
|---|---|---|
| Fonksiyon benzeri | Parantez içi | Çağrının yerine geçer |
| Derive | Yapının tamamı | Yapının yanına eklenir |
| Attribute | Argümanlar + öğe | Öğenin yerine geçer |

## proc_macro araçları

| Ad | İşi |
|---|---|
| `input.into_iter()` | `TokenTree`'ler |
| `input.to_string()` | Token'ların metni |
| `input.is_empty()` | Boş mu? |
| `"kod".parse::<TokenStream>()` | Metinden token |
| `stream.extend(other)` | Sonuna ekler |
| `iter.collect::<TokenStream>()` | Token'lardan akış |
| `group.delimiter()` | `Brace`, `Parenthesis`, `Bracket`, `None` |
| `group.stream()` | Grubun içi |
| `Group::new(delim, stream)` | Yeni grup |
| `punct.as_char()` | Karakter |
| `punct.spacing()` | `Joint` ya da `Alone` |

## Kurulum

| Dosya | İçerik |
|---|---|
| Kök `Cargo.toml` | `my_macros = { path = "my_macros" }` |
| `my_macros/Cargo.toml` | `[lib]` altında `proc-macro = true` |
| `my_macros/src/lib.rs` | Makro fonksiyonları, `pub` |
| `src/main.rs` | `use my_macros::ad;` |

## Üretirken

| Üretmek istediğin | `format!` içinde |
|---|---|
| `{` ve `}` | `{{` ve `}}` |
| Tırnaklı metin | `{name:?}` |
| Sayı sabiti | `{count}usize` |
| Liste | `vec!{items:?}` (`Vec<String>` için) |

## Tuzak: Yalnızca makro dışa açılır

Proc macro crate'i makrodan başka bir şey dışa açamaz:

```rust
use proc_macro::TokenStream;

pub fn helper() {}

#[proc_macro]
pub fn answer(_input: TokenStream) -> TokenStream {
    "42".parse().unwrap()
}
```

```text
error: `proc-macro` crate types currently cannot export any items other than functions
tagged with `#[proc_macro]`, `#[proc_macro_derive]`, or `#[proc_macro_attribute]`
 --> my_macros/src/lib.rs:3:1
  |
3 | pub fn helper() {}
  | ^^^^^^^^^^^^^^^

error: could not compile `my_macros` (lib) due to 1 previous error
```

Derive'ın uyguladığı bir trait lazımsa o trait ayrı bir crate'te durur; gerçek kütüphaneler bu yüzden çift crate'tir (`serde` ve `serde_derive`).
