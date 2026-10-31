## Her gün kullanılanlar

| Ne istiyorsun | Yazım | `n = 4728` için |
|---|---|---|
| Çift mi? | `n % 2 == 0` | `true` |
| Tek mi? | `n % 2 != 0` | `false` |
| 5'e tam bölünüyor mu? | `n % 5 == 0` | `false` |
| Son basamak | `n % 10` | 8 |
| Sondan ikinci basamak | `n / 10 % 10` | 2 |
| Sondan üçüncü basamak | `n / 100 % 10` | 7 |

Tek sayıyı `n % 2 == 1` diye sınama: `-3 % 2` değeri `-1`'dir ve şart yanlış çıkar. `!= 0` her sayıda doğrudur.

## Basamak ayırmak ve başa sarmak

```rust
fn main() {
    let n = 4728;
    println!("{}", n % 10);
    println!("{}", n / 10 % 10);
    println!("{}", n / 100 % 10);
    println!("{}", (0 - 1) % 7);
    println!("{}", (0_i32 - 1).rem_euclid(7));
}
```

```text
8
2
7
-1
6
```

Son iki satır aynı soruyu soruyor: "Pazartesi'nin (0) bir gün öncesi hangi gün?" `%` eksi verir, `rem_euclid` doğru
gün olan 6'yı (Pazar) verir. Başa saran saymada sayı eksiye düşebiliyorsa `rem_euclid` kullan.

## Sıfıra kalan

Sıfıra bölmek gibi, sıfıra göre kalan almak da programı durdurur:

```rust
fn main() {
    let items = "".len();
    println!("{}", 10 % items);
}
```

```text
thread 'main' panicked at main.rs:3:20:
attempt to calculate the remainder with a divisor of zero
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```
