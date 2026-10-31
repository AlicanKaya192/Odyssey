## Biçim dizisinin düzeni

Süslü parantezin içi şu sırayla yazılır, hepsi isteğe bağlıdır:

```text
{ad : dolgu hizalama işaret # 0 genişlik .basamak tür}
```

## Hepsi bir arada

| Yazım | Değer | Sonuç |
|---|---|---|
| `{}` | `42` | `42` |
| `{name}` | `name = "Ada"` | `Ada` |
| `{0} {1} {0}` | `"a", "b"` | `a b a` |
| `{:.2}` | `3.14159` | `3.14` |
| `{:5}` | `42` | `   42` |
| `{:<5}` | `42` | `42   ` |
| `{:^5}` | `"ab"` | ` ab  ` |
| `{:05}` | `42` | `00042` |
| `{:*^7}` | `"ab"` | `**ab***` |
| `{:+}` | `42` | `+42` |
| `{:>8.2}` | `3.5` | `    3.50` |
| `{:b}` | `10` | `1010` |
| `{:o}` | `10` | `12` |
| `{:x}` `{:X}` | `255` | `ff` `FF` |
| `{:#x}` | `255` | `0xff` |
| `{:08b}` | `10` | `00001010` |
| `{:e}` | `1500.0` | `1.5e3` |
| `{:?}` | `"Ada"` | `"Ada"` |
| `{:#?}` | Demet, struct | Çok satırlı |

## Genişlik değişkenden gelebilir

Genişlik ya da basamak çalışırken belli oluyorsa adın sonuna `$` konur:

```rust
fn main() {
    let width = 6;
    let digits = 2;
    println!("[{:>width$}]", "ab");
    println!("[{:.digits$}]", 3.14159);
    println!("[{:>width$.digits$}]", 3.14159);
}
```

```text
[    ab]
[3.14]
[  3.14]
```

## Yazan makrolar

| Makro | Nereye yazar | Satır sonu |
|---|---|---|
| `println!` | Standart çıktı | Var |
| `print!` | Standart çıktı | Yok |
| `eprintln!` | Standart hata | Var |
| `eprint!` | Standart hata | Yok |
| `format!` | Yazmaz, `String` verir | Yok |

Hata mesajları `eprintln!` ile yazılır: Çıktı bir dosyaya yönlendirilse bile ekranda kalır.
