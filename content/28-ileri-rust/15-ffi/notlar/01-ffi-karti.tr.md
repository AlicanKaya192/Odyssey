## Tür eşlemesi

| C | Rust |
|---|---|
| `int` | `c_int` |
| `unsigned int` | `c_uint` |
| `long` | `c_long` |
| `char` | `c_char` |
| `double` | `c_double` |
| `size_t` | `usize` |
| `void *` | `*mut c_void` |
| `const char *` | `*const c_char` |
| `int32_t` | `i32` |
| `void` (dönüş) | Dönüş türü yok |
| İşlev işaretçisi | `extern "C" fn(...)` |
| Boş olabilen işlev işaretçisi | `Option<extern "C" fn(...)>` |

Hepsi `std::ffi` içinde. `long` Windows'ta 32, Linux'ta 64 bittir; `i64` yazmak bu yüzden yanlış olur.

## Metin türleri

| Tür | Sahibi | Sonu NUL | Ne zaman |
|---|---|---|---|
| `String` | Rust | Hayır | Rust içinde |
| `&str` | Ödünç | Hayır | Rust içinde |
| `CString` | Rust | Evet | C'ye göndermek |
| `&CStr` | Ödünç | Evet | C'den almak, sabit |
| `OsString` | Rust | Hayır | İşletim sistemi yolları |

## Dönüşümler

| Nereden, nereye | Yazım |
|---|---|
| `&str` → `CString` | `CString::new(text)?` |
| `CString` → işaretçi | `text.as_ptr()` |
| Sabit → `&CStr` | `c"hello"` |
| İşaretçi → `&CStr` | `unsafe { CStr::from_ptr(p) }` |
| `&CStr` → `&str` | `text.to_str()?` |
| `&CStr` → metin | `text.to_string_lossy()` |

## Bildirim yazımı

| İhtiyaç | Yazım |
|---|---|
| C'den fonksiyon | `unsafe extern "C" { fn f(); }` |
| Her girdi için güvenli | `safe fn f();` |
| C'ye açık fonksiyon | `#[unsafe(no_mangle)] pub extern "C" fn f()` |
| C uyumlu yapı | `#[repr(C)] struct S { ... }` |
| C uyumlu `enum` | `#[repr(C)] enum E { ... }` |
| Kütüphane | `crate-type = ["cdylib"]` |

## Sık hata

Geçici `CString`'in işaretçisini almak:

```rust
use std::ffi::{CString, c_char};

fn main() {
    let pointer: *const c_char = CString::new("hi").unwrap().as_ptr();
    println!("{pointer:?}");
}
```

```text
warning: this creates a dangling pointer because temporary `CString` is dropped at end
of statement
 --> main.rs:4:62
  |
4 |     let pointer: *const c_char = CString::new("hi").unwrap().as_ptr();
  |                                  --------------------------- ^^^^^^ pointer created
  here
  |                                  |
  |                                  this `CString` is dropped at end of statement
  |
  = help: bind the `CString` to a variable such that it outlives the pointer returned by
    `as_ptr`
  = note: a dangling pointer is safe, but dereferencing one is undefined behavior
  = note: returning a pointer to a local variable will always result in a dangling
    pointer
  = note: for more information, see
    <https://doc.rust-lang.org/reference/destructors.html>
  = note: `#[warn(dangling_pointers_from_temporaries)]` on by default
```

`CString` satır sonunda düşer ve işaretçi boşa düşer. Önce `let text = CString::new(...)?;`, sonra `text.as_ptr()`.
