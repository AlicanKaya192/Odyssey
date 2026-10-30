## Aritmetik

```rust
fn main() {
    println!("{}", 7 + 2);
    println!("{}", 7 - 2);
    println!("{}", 7 * 2);
    println!("{}", 7 / 2);
    println!("{}", 7 % 2);
    println!("{}", 7.0 / 2.0);
    println!("{}", -7 / 2);
    println!("{}", -7 % 2);
}
```

```text
9
5
14
3
1
3.5
-3
-1
```

**Tam sayı bölmesi ondalık kısmı atar:** `7 / 2` değeri `3`'tür, `3.5` değil. Ondalık sonuç için `7.0 / 2.0` yazılır. `%` kalanı verir.

Eksi sayıda dikkat: `-7 / 2` değeri `-3`, `-7 % 2` değeri `-1`'dir. Sonuç sıfıra doğru kesilir.

## Sık kullanılan sayı metotları

| Metot | Örnek | Sonuç |
|---|---|---|
| `abs` | `(-5_i32).abs()` | 5 |
| `pow` | `2_i32.pow(10)` | 1024 |
| `min` / `max` | `3.min(9)` | 3 |
| `sqrt` | `9.0_f64.sqrt()` | 3.0 |
| `round` | `2.5_f64.round()` | 3.0 |
| `floor` / `ceil` | `2.5_f64.floor()` | 2.0 |

Metot çağırırken sayının türünü belirtmen gerekebilir: `9.0.sqrt()` derlenmez, çünkü derleyici `f32` mü `f64` mü bilemez. Bu yüzden `9.0_f64` yazılır.

## Karşılaştırma ve mantık

| İşaret | Anlamı |
|---|---|
| `==` `!=` | Eşit, eşit değil |
| `<` `>` `<=` `>=` | Küçük, büyük, küçük eşit, büyük eşit |
| `&&` <code>&#124;&#124;</code> `!` | Ve, ya da, değil |

`&&` ve `||` kısa devre yapar: Sol taraf sonucu belirlediyse sağ taraf hiç çalışmaz.

## Karşılaştırmada tür aynı olmalı

`let a: i32 = 5; let b: i64 = 5; a == b` derlenmez. Rust burada da `i32`'yi `i64`'e kendiliğinden çevirmez: `a as i64 == b` yazılır.
