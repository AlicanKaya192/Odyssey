## Hangisini seçmeli?

| Durum | Kullan | Örnek |
|---|---|---|
| Değer hiç değişmiyor | `let` | `let name = "Ada";` |
| Aynı şey güncelleniyor | `let mut` | Döngüdeki toplam |
| Değer başka biçime dönüşüyor | Gölgeleme | Metinden sayıya |
| Program boyunca sabit | `const` | `const MAX_USERS: u32 = 100;` |

## Sık yapılan hatalar

**`mut`'u unutmak.** Hata kodu `E0384`. Mesaj `help:` satırında çözümü verir.

**Gerekmeyen `mut`.** Program çalışır ama uyarı alırsın. Uyarıları temizlemek iyi alışkanlıktır.

```rust
fn main() {
    let mut name = "Ada";
    println!("{name}");
}
```

```text
Ada
```

Uyarı metnini yukarıda göremezsin çünkü program başarıyla çalıştı ve uyarı derleme sırasında çıkıyor. Kendi
projende `cargo build` sırasında `variable does not need to be mutable` yazar.

**Değer vermeden kullanmak.** `let x;` yazabilirsin ama değer vermeden okuyamazsın:

```rust
fn main() {
    let x: i32;
    println!("{x}");
}
```

```text
error[E0381]: used binding `x` isn't initialized
 --> main.rs:3:16
  |
2 |     let x: i32;
  |         - binding declared here but left uninitialized
3 |     println!("{x}");
  |                ^ `x` used here but it isn't initialized
  |
help: consider assigning a value
  |
2 |     let x: i32 = 42;
  |                ++++
```

Rust hiçbir zaman "rastgele bir değer" okutmaz. Bu, C'de çok yaygın bir hata sınıfını tamamen ortadan kaldırır.

## Gölgeleme tuzağı

Bir bloğun içindeki `let` dıştakini değiştirmez, yalnızca örter:

```rust
fn main() {
    let total = 1;
    {
        let total = total + 10;
        println!("inside: {total}");
    }
    println!("outside: {total}");
}
```

```text
inside: 11
outside: 1
```

Dıştaki değeri gerçekten değiştirmek istiyorsan `let` yazmadan atama yaparsın (`total = total + 1;`) ve dıştaki `mut` olmalıdır.
