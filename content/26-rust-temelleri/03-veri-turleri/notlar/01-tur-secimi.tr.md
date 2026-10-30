## Hangi türü seçmeli?

| İhtiyaç | Tür | Neden |
|---|---|---|
| Sıradan tam sayı | `i32` | Varsayılan, çoğu iş için yeterli |
| Sıra numarası, uzunluk | `usize` | `.len()` ve dizi erişimi bunu ister |
| Bayt, küçük pozitif değer | `u8` | 0–255 |
| Çok büyük sayı, zaman damgası | `i64` / `u64` | 9 kentilyon civarı |
| Ondalıklı | `f64` | Hassas ve hızlı |
| Evet/hayır | `bool` | |
| Tek harf | `char` | Dört bayt, her alfabeyi tutar |

## Bayt boyutları

```rust
fn main() {
    use std::mem::size_of;
    println!("u8:    {}", size_of::<u8>());
    println!("i32:   {}", size_of::<i32>());
    println!("f64:   {}", size_of::<f64>());
    println!("char:  {}", size_of::<char>());
    println!("bool:  {}", size_of::<bool>());
    println!("usize: {}", size_of::<usize>());
}
```

```text
u8:    1
i32:   4
f64:   8
char:  4
bool:  1
usize: 8
```

`std::mem::size_of` bir türün bellekte kaç bayt tuttuğunu söyler. Ölçüm bu makinede alındı; `usize` 64 bitlik
bilgisayarda 8 bayttır.

## Sayı yazım biçimleri

| Yazım | Değer | Anlamı |
|---|---|---|
| `1_000_000` | bir milyon | Alt çizgi okumayı kolaylaştırır |
| `0xFF` | 255 | On altılık taban |
| `0b1010` | 10 | İkilik taban |
| `0o17` | 15 | Sekizlik taban |
| `b'A'` | 65 | Karakterin bayt değeri |
| `7u8` | 7 | Tür sayının üstünde yazılır |
| `2.5e3` | 2500.0 | Bilimsel gösterim |

## Metin türleri nerede?

Metin (`String`, `&str`) burada yok, çünkü sahipliği anlamadan anlatılamaz. Sekizinci bölümde kendi başına ele alınıyor.
