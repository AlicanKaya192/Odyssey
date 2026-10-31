# İşleçler (Operatörler)

`2 + 3` yazınca `+` bir **işleç** (operator), yani "bu değerlerle şunu yap" diyen işarettir. Bu bölümde hesap yapan,
karşılaştıran ve şartları birleştiren bütün işleçleri topluyoruz. Çoğu her dilde aynıdır ama Rust'ın birkaç
sürprizi var: Üs işleci yok, `++` yok.

## Aritmetik

```rust
fn main() {
    println!("{}", 7 + 2);
    println!("{}", 7 - 2);
    println!("{}", 7 * 2);
    println!("{}", 7 / 2);
    println!("{}", 7 % 2);
}
```

```text
9
5
14
3
1
```

| İşleç | Anlamı | Örnek | Sonuç |
|---|---|---|---|
| `+` | Toplama | `7 + 2` | 9 |
| `-` | Çıkarma | `7 - 2` | 5 |
| `*` | Çarpma | `7 * 2` | 14 |
| `/` | Bölme | `7 / 2` | 3 |
| `%` | Kalan | `7 % 2` | 1 |

Dördüncü satıra dikkat: `7 / 2` değeri 3'tür, 3,5 değil.

## Tam sayı bölmesi

İki taraf da tam sayıysa sonuç da tam sayıdır ve ondalık kısım atılır. Ondalıklı sonuç için iki tarafı da bölmeden
**önce** çevirirsin:

```rust
fn main() {
    let a = 7;
    let b = 2;
    println!("{}", a / b);
    println!("{}", a as f64 / b as f64);
    println!("{}", (a / b) as f64);
}
```

```text
3
3.5
3
```

Üçüncü satır yine 3 verdi: `(a / b)` önce bölüyor, ondalık o anda kayboluyor, sonra çevirmenin faydası kalmıyor.

## Kalan: `%`

`%` bölme işleminden kalanı verir. İlk bakışta seyrek işe yarayacak gibi durur ama sürekli karşına çıkar:

```rust
fn main() {
    let n = 472;
    println!("{}", n % 2 == 0);
    println!("{}", n % 10);
    let minutes = 135;
    println!("{} h {} min", minutes / 60, minutes % 60);
    println!("{}", (5 + 4) % 7);
}
```

```text
true
2
2 h 15 min
2
```

| Soru | Yazım | Neden |
|---|---|---|
| Sayı çift mi? | `n % 2 == 0` | İkiye bölümden kalan yok |
| Son basamak ne? | `n % 10` | Ona bölümden kalan son basamak |
| Kaç saat kaç dakika? | `m / 60` ve `m % 60` | Bölüm saat, kalan dakika |
| Pazartesi'den 9 gün sonra? | `(0 + 9) % 7` | Başa saran sayma |

Eksi sayılarda kalan, bölünenin işaretini alır. Her zaman sıfır ya da pozitif kalan istiyorsan `rem_euclid` vardır.
`%` ondalıklı sayılarda da çalışır:

```rust
fn main() {
    println!("{}", -7 / 2);
    println!("{}", -7 % 2);
    println!("{}", (-7_i32).rem_euclid(2));
    println!("{}", 7.5 % 2.0);
}
```

```text
-3
-1
1
1.5
```

## Üs almak: işleç yok

Birçok dilde üs için `**` ya da `^` yazılır. Rust'ta üs işleci yoktur, metot çağrılır: Tam sayıda `pow`, ondalıkta
tam sayı üs için `powi`, ondalık üs için `powf`.

```rust
fn main() {
    println!("{}", 2_i32.pow(10));
    println!("{}", 2.0_f64.powi(3));
    println!("{}", 9.0_f64.powf(0.5));
    println!("{}", 2 ^ 3);
}
```

```text
1024
8
3
1
```

Son satır bir tuzak: `2 ^ 3` derlenir ve **1** verir. `^` üs değil, bitleri karşılaştıran başka bir işleçtir. Derleyici
uyarmaz, çünkü kod geçerlidir.

## Bileşik atama

Bir değişkeni kendi değeri üzerinden değiştirmek o kadar sık olur ki kısa yazımı vardır. `score += 5`,
`score = score + 5` demektir. Değişken `mut` olmalı.

```rust
fn main() {
    let mut score = 10;
    score += 5;
    println!("{score}");
    score -= 3;
    println!("{score}");
    score *= 2;
    println!("{score}");
    score /= 4;
    println!("{score}");
    score %= 4;
    println!("{score}");
}
```

```text
15
12
24
6
2
```

Rust'ta `++` ve `--` yoktur. Başka bir dilden alışkanlıkla yazarsan derleyici ne yapman gerektiğini söyler:

```rust
fn main() {
    let mut x = 1;
    x++;
    println!("{x}");
}
```

```text
error: Rust has no postfix increment operator
 --> main.rs:3:6
  |
3 |     x++;
  |      ^^ not a valid postfix operator
  |
help: use `+= 1` instead
  |
3 -     x++;
3 +     x += 1;
  |
```

## Karşılaştırma

Karşılaştırma işleçleri iki değere bakar ve bir `bool` üretir. Dikkat: `=` atar, `==` karşılaştırır.

```rust
fn main() {
    println!("{}", 5 == 5);
    println!("{}", 5 != 5);
    println!("{}", 3 < 7);
    println!("{}", 7 <= 7);
    println!("{}", "apple" == "apple");
    println!("{}", "apple" < "banana");
    println!("{}", 'a' < 'b');
}
```

```text
true
false
true
true
true
true
true
```

| İşleç | Anlamı |
|---|---|
| `==` | Eşit |
| `!=` | Eşit değil |
| `<` `>` | Küçük, büyük |
| `<=` `>=` | Küçük ya da eşit, büyük ya da eşit |

Metinler sözlük sırasıyla karşılaştırılır. İki taraf **aynı türden** olmalı; Rust burada da kendiliğinden çevirmez:

```rust
fn main() {
    let a: i32 = 5;
    let b: i64 = 5;
    println!("{}", a == b);
}
```

```text
error[E0308]: mismatched types
 --> main.rs:4:25
  |
4 |     println!("{}", a == b);
  |                    -    ^ expected `i32`, found `i64`
  |                    |
  |                    expected because this is `i32`
  |
help: you can convert `a` from `i32` to `i64`, matching the type of `b`
  |
4 |     println!("{}", i64::from(a) == b);
  |                    ++++++++++ +
```

Çözüm `a as i64 == b`. Karşılaştırmalar matematikteki gibi zincirlenmez:

```rust
fn main() {
    let x = 5;
    println!("{}", 1 < x < 10);
}
```

```text
error: comparison operators cannot be chained
 --> main.rs:3:22
  |
3 |     println!("{}", 1 < x < 10);
  |                      ^   ^
  |
help: split the comparison into two
  |
3 |     println!("{}", 1 < x && x < 10);
  |                          ++++
```

Doğrusu şartı ikiye bölüp `&&` ile bağlamaktır:

```rust
fn main() {
    let x = 5;
    println!("{}", 1 < x && x < 10);
}
```

```text
true
```

## Mantık: `&&`, `||`, `!`

| İşleç | Anlamı | Ne zaman `true` |
|---|---|---|
| `&&` | Ve | İki taraf da `true` ise |
| <code>&#124;&#124;</code> | Ya da | En az biri `true` ise |
| `!` | Değil | Değer `false` ise |

```rust
fn main() {
    let age = 20;
    let member = false;
    println!("{}", age >= 18 && member);
    println!("{}", age >= 18 || member);
    println!("{}", !member);
}
```

```text
false
true
true
```

`&&` ve `||` **kısa devre** (short circuit) yapar: Sol taraf sonucu belirlediyse sağ taraf hiç çalıştırılmaz. Bu bir
hız ayrıntısı değil, güvenlik aracıdır. Tam sayıyı sıfıra bölmek programı durdurur:

```rust
fn main() {
    let items = "".len();
    println!("{}", 10 / items);
}
```

```text
thread 'main' panicked at main.rs:3:20:
attempt to divide by zero
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

Önce sıfır olmadığına bakarsan bölme hiç çalışmaz:

```rust
fn main() {
    let items = "".len();
    println!("{}", items != 0 && 10 / items > 1);
    println!("{}", items == 0 || 10 / items > 1);
}
```

```text
false
true
```

Buradaki `"".len()` boş metnin uzunluğu, yani 0. Sıfırı böyle dolaylı yazdık, çünkü `10 / 0`'ı derleyici doğrudan reddeder.

## Hangisi önce yapılır?

Matematikteki gibi çarpma toplamadan önce gelir. Sıra bir ifadede karışıyorsa parantez yaz; hem doğru çalışır hem de
okuyan düşünmek zorunda kalmaz.

```rust
fn main() {
    println!("{}", 2 + 3 * 4);
    println!("{}", (2 + 3) * 4);
    println!("{}", 10 - 4 - 3);
    println!("{}", true || false && false);
    println!("{}", (true || false) && false);
    println!("{}", -2_i32.pow(2));
    println!("{}", (-2_i32).pow(2));
}
```

```text
14
20
3
true
false
-4
4
```

İki sonuca dikkat. `&&`, `||`'den önce yapıldığı için dördüncü satır `true` verdi. Son iki satırda ise metot çağrısı eksi
işaretinden önce gelir: `-2_i32.pow(2)` "2'nin karesinin eksilisi" demektir. Tam tablo ders notunda.

## Özet

- `+ - * / %`: `/` tam sayıda ondalığı atar, `%` kalanı verir.
- Ondalıklı bölme için iki taraf da **bölmeden önce** çevrilir: `a as f64 / b as f64`.
- Üs işleci yok: `pow`, `powi`, `powf`. `^` üs değildir.
- `+=`, `-=`, `*=`, `/=`, `%=` var; `++` yok.
- `==`, `!=`, `<`, `>`, `<=`, `>=` bir `bool` üretir; iki taraf aynı türden olmalı, zincir yazılmaz.
- `&&` ve `||` kısa devre yapar; bu, sıfıra bölme gibi hatalardan korur.
