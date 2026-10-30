## Fonksiyon kendini çağırabilir

Bir fonksiyonun kendini çağırmasına **özyineleme** (recursion) denir. İki şey gerekir: işi küçülten adım ve
durduran koşul.

```rust
fn factorial(n: u64) -> u64 {
    if n <= 1 {
        return 1;
    }
    n * factorial(n - 1)
}

fn main() {
    println!("{}", factorial(5));
    println!("{}", factorial(20));
}
```

```text
120
2432902008176640000
```

`factorial(5)` şöyle açılır: `5 * factorial(4)`, o da `4 * factorial(3)`, ... ta ki `n` 1 olana dek. Sonra sonuçlar
geri dönerken çarpılır.

## Durma koşulu unutulursa

Her çağrı **yığın** (stack) adı verilen bellek alanında yer kaplar. Hiç durmayan özyineleme bu alanı doldurur ve program
yığın taşması ile ölür. Rust bunu derlemede yakalamaz ama güvenli biçimde durur; bellekte başka bir yeri bozmaz.

## Tür seçimi yine önemli

`u64` bile sonsuz değil: `factorial(21)` `u64`'e sığmaz ve geliştirme derlemesinde panik verir. Büyük sayılarla çalışırken
sınırları düşün.

## Özyineleme mi, döngü mü?

Çoğu işi ikisi de yapar. Rust'ta döngü genellikle daha hızlıdır ve yığını doldurmaz. Özyineleme ağaç gibi kendini tekrar
eden yapılarda doğal olur. Döngüleri sonraki bölümde görüyoruz.
