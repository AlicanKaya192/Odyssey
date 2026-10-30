`println!` metne değer koymaktan fazlasını yapar. İki nokta üst üsteden sonra biçim yazılabilir.

```rust
fn main() {
    let pi = 3.14159;
    let n = 7;
    println!("[{:.2}]", pi);
    println!("[{:>6}]", n);
    println!("[{:<6}]", n);
    println!("[{:^6}]", n);
    println!("[{:03}]", n);
    println!("{0} {0} {1}", n, pi);
    println!("{{{n}}}");
}
```

```text
[3.14]
[     7]
[7     ]
[  7   ]
[007]
7 7 3.14159
{7}
```

## Kart

| Yazım | Sonuç | Ne yapar |
|---|---|---|
| `{x}` | değer | Değişkeni doğrudan yazar |
| `{0} {0}` | iki kez | Aynı değeri sırasıyla çağırır |
| `{:.2}` | `3.14` | Ondalıktan sonra iki basamak |
| `{:>6}` | sağa yaslı | 6 karakter genişlikte |
| `{:<6}` | sola yaslı | 6 karakter genişlikte |
| `{:^6}` | ortalı | 6 karakter genişlikte |
| `{:03}` | `007` | Başı sıfırla doldurur |
| `{:?}` | hata ayıklama | Değeri programcı için gösterir |

`{:?}` ileride çok işimize yarayacak: Listeleri ve yapıları doğrudan yazdırır. Normal `{}` onları
kabul etmez.

## Süslü parantezin kendisi

Metinde gerçek bir süslü parantez yazmak için iki kez yazarsın: `{{` ve `}}`.

## print!, eprintln!

| Makro | Ne yapar |
|---|---|
| `println!` | Yazar ve alt satıra geçer |
| `print!` | Yazar, alt satıra geçmez |
| `eprintln!` | Hata kanalına yazar |
| `format!` | Yazmaz, metin olarak geri verir |

`eprintln!` hata mesajları içindir. Program çıktısı bir dosyaya yönlendirilse bile hata mesajı ekranda kalır.
