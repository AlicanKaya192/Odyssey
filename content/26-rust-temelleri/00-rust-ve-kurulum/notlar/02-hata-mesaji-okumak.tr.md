Rust öğrenirken en çok vakit geçireceğin yer derleyicinin mesajlarıdır. Hepsi aynı kalıpta.

```rust
fn main() {
    println!("{} and {}", 1);
}
```

```text
error: 2 positional arguments in format string, but there is 1 argument
 --> main.rs:2:15
  |
2 |     println!("{} and {}", 1);
  |               ^^     ^^   -
```

## Parçalar

| Parça | Anlamı |
|---|---|
| `error` | Program oluşmadı, düzeltmen gerekiyor |
| `warning` | Program oluştu ama derleyici bir şeyi garip buldu |
| `[E0599]` gibi kod | Hatanın kimliği |
| `-->` | Dosya, satır, sütun |
| `^^^^` | Sorunlu parça |
| `note:` | Ek açıklama |
| `help:` | Önerilen düzeltme |

## Hata kodunu açmak

Bir hatanın köşeli parantezli kodu varsa derleyici ondan uzun bir açıklama da verebilir. Terminale
şunu yaz:

```bash
rustc --explain E0599
```

Çıktı hatanın ne olduğunu örnekle anlatır ve internet istemez.

## İyi bir alışkanlık

1. Yalnızca ilk hatayı oku.
2. `-->` satırındaki yere git.
3. `help:` varsa önce onu dene.
4. Yeniden derle; hata sayısı çoğu zaman bir anda azalır.

Uyarıları da oku. Program çalışsa bile uyarılar çoğu zaman gerçek bir unutkanlığı gösterir,
örneğin hiç kullanmadığın bir değişkeni.
