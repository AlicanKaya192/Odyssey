# Veri Türleri

Bellekte her şey bitlerden, yani 0 ve 1'lerden oluşur. Aynı bitler bir sayı da olabilir, bir harf de.
**Tür** (type), bir değerin neyi temsil ettiğini ve onunla ne yapılabileceğini söyler.

Rust **statik türlü** bir dildir: Her değişkenin türü derleme anında bellidir. Yazmak zorunda
değilsin, derleyici çoğu zaman kendisi çıkarır. Ama çıkaramazsa sorar.

```rust
fn main() {
    let x = 2;
    let total: i32 = 40;
    println!("{}", x + total);
}
```

```text
42
```

`let total: i32 = 40;` satırındaki `: i32` bir **tür belirtimidir**. `x` için yazmadık, derleyici çıkardı.

## Tam sayılar

Tam sayı türleri iki soruya cevap verir: Eksi olabilir mi? Kaç bit tutuyor?

| Bit | İşaretli (eksi olabilir) | İşaretsiz (0 ve üstü) |
|---|---|---|
| 8 | `i8` | `u8` |
| 16 | `i16` | `u16` |
| 32 | `i32` | `u32` |
| 64 | `i64` | `u64` |
| 128 | `i128` | `u128` |
| Makineye göre | `isize` | `usize` |

`i` "integer" (tam sayı), `u` "unsigned" (işaretsiz) demektir. Bit arttıkça sığan sayı büyür. Her türün
sınırını doğrudan sorabilirsin:

```rust
fn main() {
    println!("u8:  {} to {}", u8::MIN, u8::MAX);
    println!("i8:  {} to {}", i8::MIN, i8::MAX);
    println!("i32: {} to {}", i32::MIN, i32::MAX);
}
```

```text
u8:  0 to 255
i8:  -128 to 127
i32: -2147483648 to 2147483647
```

Tür yazmazsan tam sayılar `i32` olur; çoğu iş için doğru seçim budur. Sıra numaraları ve uzunluklar için
Rust `usize` kullanır: Bu makinenin belleğini gösterebilecek kadar büyük bir sayıdır, 64 bitlik bilgisayarda 64 bittir.

## Taşma: sınır aşılırsa ne olur?

`u8` en fazla 255 tutar. 255'e 1 eklersek? Derleyici sabit bir işlemi görürse doğrudan reddeder. Değer
program çalışırken ortaya çıkarsa geliştirme derlemesinde program **panikler**, yani hata mesajıyla durur:

```rust
fn main() {
    let text = "hello";
    let mut small = 251u8;
    small += text.len() as u8;
    println!("{small}");
}
```

```text
thread 'main' panicked at main.rs:4:5:
attempt to add with overflow
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

Burada `.len()` metnin uzunluğunu veriyor ve `as u8` onu `u8`'e çeviriyor, böylece sayıyı derleyici önceden
göremiyor. Programın son hâli derlenirken (`--release` ayarı, Cargo bölümünde göreceğiz) bu denetim kapalıdır
ve sayı başa sarar (255 + 1 = 0). Bu fark yüzünden
taşabilecek yerde açık davranmak en iyisidir:

```rust
fn main() {
    let big: u8 = 250;
    println!("{:?}", big.checked_add(10));
    println!("{}", big.wrapping_add(10));
    println!("{}", big.saturating_add(10));
}
```

```text
None
4
255
```

| Metot | Ne yapar |
|---|---|
| `checked_add` | Taşarsa `None` verir (`Option`, ileride göreceğiz) |
| `wrapping_add` | Başa sarar |
| `saturating_add` | Sınırda kalır |

## Ondalıklı sayılar

İki tür var: `f32` ve `f64`. Varsayılan `f64`'tür ve çoğu işte onu kullanırsın.

```rust
fn main() {
    let half = 7.0 / 2.0;
    println!("{half}");
    println!("{}", 0.1 + 0.2);
    let difference: f64 = (0.1 + 0.2 - 0.3_f64).abs();
    println!("{}", difference < 0.000001);
}
```

```text
3.5
0.30000000000000004
true
```

İkinci satıra dikkat: `0.1 + 0.2` tam olarak `0.3` değil. Bu Rust'a özgü değil, bilgisayarların ondalık
sayıları iki tabanında tutmasından gelir ve bütün dillerde vardır. Bu yüzden ondalık sayıları `==` ile
karşılaştırmak yerine aradaki farkın çok küçük olup olmadığına bakılır. Para gibi kesin hesaplarda tam sayı
(kuruş) kullanılır.

## Sayı türleri kendiliğinden karışmaz

Birçok dilin aksine Rust `i32` ile `f64`'ü kendiliğinden toplamaz:

```rust
fn main() {
    let count = 3;
    let price = 2.5;
    println!("{}", count * price);
}
```

```text
error[E0277]: cannot multiply `{integer}` by `{float}`
 --> main.rs:4:26
  |
4 |     println!("{}", count * price);
  |                          ^ no implementation for `{integer} * {float}`
  |
  = help: the trait `Mul<{float}>` is not implemented for `{integer}`
  = help: the following other types implement trait `Mul<Rhs>`:
            `&f128` implements `Mul<f128>`
            `&f128` implements `Mul`
            `&f16` implements `Mul<f16>`
            `&f16` implements `Mul`
            `&f32` implements `Mul<f32>`
            `&f32` implements `Mul`
            `&f64` implements `Mul<f64>`
            `&f64` implements `Mul`
          and 57 others
```

Dönüşümü sen açıkça yazarsın. `as` en basit yoldur:

```rust
fn main() {
    let count = 3;
    let price = 2.5;
    println!("{}", count as f64 * price);
    println!("{}", 9.99_f64 as i32);
    println!("{}", 300_i32 as u8);
}
```

```text
7.5
9
44
```

Son satıra dikkat et. `as` kısa bir türe çevirirken değeri **sessizce keser**: 300 sayısı `u8`'e sığmaz ve 44
olur. Ondalıktan tam sayıya çevirirken de ondalık kısım atılır, yuvarlanmaz. Bu yüzden `as`'ı sonucun sığacağından
emin olduğunda kullan. Güvenli dönüşümleri ileride göreceğiz.

## Mantıksal değer: bool

`bool` yalnızca iki değer alır: `true` ve `false`. Karşılaştırmaların sonucudur.

```rust
fn main() {
    let age = 20;
    let adult = age >= 18;
    println!("{adult}");
    println!("{}", adult && age < 30);
    println!("{}", !adult || age == 20);
}
```

```text
true
true
true
```

`&&` "ve", `||` "ya da", `!` "değil" demektir. Bütün işleçleri bir sonraki bölümde ele alıyoruz.

## Karakter: char

`char` tek bir karakterdir ve **tek tırnakla** yazılır. Rust'ta `char` 4 bayttır ve Türkçe harfleri, emojileri
de tutabilir:

```rust
fn main() {
    let letter = 'R';
    let crab = '\u{1F980}';
    println!("{letter} {crab}");
    println!("{}", std::mem::size_of::<char>());
}
```

```text
R 🦀
4
```

Tek tırnak `char`, çift tırnak metindir: `'a'` ile `"a"` farklı türlerdir.

## Metin: `&str` ve `String`

Çift tırnaklı yazı da bir değerdir, değişkene konabilir. Rust'ta iki metin türü var, çünkü metin iki farklı
yerde durabilir: Programın içine gömülü olarak ya da program çalışırken ayrılan bellekte.

```rust
fn main() {
    let city = "Izmir";
    let mut message = String::from("Hello");
    message.push_str(", ");
    message.push_str(city);
    println!("{message}");
}
```

```text
Hello, Izmir
```

| | `&str` | `String` |
|---|---|---|
| Nasıl yazılır | `"Izmir"` | `String::from("Hello")` |
| Değişebilir mi | Hayır | Evet, `mut` ile |
| Ne zaman | Sabit metin, yalnızca okumak | Program çalışırken oluşan ya da büyüyen metin |

Neden iki tür olduğunu Sahiplik ve Dilimler bölümlerinde göreceğiz. Şimdilik şu kural yeter: Yazıp geçeceksen
`"..."`, değiştireceksen `String`.

Metin üreten en rahat yol `format!`: `println!` gibi yazılır ama ekrana basmak yerine bir `String` verir.
Sayıyı metne `to_string` çevirir.

```rust
fn main() {
    let first = "Ada";
    let age = 36;
    let label = format!("{first} ({age})");
    println!("{label}");
    let digits = age.to_string();
    println!("{}", digits);
}
```

```text
Ada (36)
36
```

Sık kullanılan birkaç metot:

```rust
fn main() {
    let text = "  Rust is fun  ";
    println!("[{}]", text.trim());
    println!("{}", text.to_uppercase());
    println!("{}", text.contains("is"));
    println!("{}", text.replace("fun", "fast"));
    println!("{}", "abc" == "abc");
    println!("{}", "seker".len());
    println!("{}", "şeker".len());
    println!("{}", "şeker".chars().count());
}
```

```text
[Rust is fun]
  RUST IS FUN
true
  Rust is fast
true
5
6
5
```

Son iki satıra dikkat: `len` harf değil **bayt** sayar ve `ş` iki bayt tuttuğu için `"şeker"` 6 çıkar. Harf saymak
için `chars().count()` yazılır.

## Birden fazla değer: demet

**Demet** (tuple) farklı türlerden sabit sayıda değeri tek bir değerde toplar:

```rust
fn main() {
    let point = (3, 4.5, true);
    println!("{}", point.0);
    println!("{:?}", point);
    let (x, y, on) = point;
    println!("{x} {y} {on}");
}
```

```text
3
(3, 4.5, true)
3 4.5 true
```

Parçalara `.0`, `.1` ile ya da `let` ile açarak ulaşılır. Açmaya **çözümleme** (destructuring) denir. `{:?}`
biçimi demeti olduğu gibi yazdırır; normal `{}` demeti kabul etmez.

Hiç değer içermeyen demet `()` özel bir türdür, adı **birim** (unit): "anlamlı bir değer yok" demektir.

## Sabit listeler: dizi

**Dizi** (array) aynı türden, **sabit sayıda** değerdir:

```rust
fn main() {
    let days: [i32; 3] = [10, 20, 30];
    println!("{}", days[0]);
    println!("{}", days.len());
    println!("{:?}", days);
    let zeros = [0; 4];
    println!("{:?}", zeros);
}
```

```text
10
3
[10, 20, 30]
[0, 0, 0, 0]
```

Türü `[i32; 3]`: "3 tane `i32`". Sıra numarası 0'dan başlar. Boyut türün parçasıdır, yani dizi büyüyüp küçülemez.
Büyüyebilen liste `Vec`'tir, onu ileride göreceğiz.

Dizinin dışına çıkan bir sıra numarası programı durdurur. Rust böylece komşu belleği okumayı engeller:

```rust
fn main() {
    let days = [10, 20, 30];
    let position = days.len() + 1;
    println!("{}", days[position]);
}
```

```text
thread 'main' panicked at main.rs:4:20:
index out of bounds: the len is 3 but the index is 4
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

Bu **panik** bir hatadır ama kontrollüdür: Program saçma veriyle devam etmek yerine durur ve nerede durduğunu söyler.

## Özet

- Her değerin türü derlemede bellidir, çoğu zaman derleyici çıkarır.
- Tam sayılar `i32`, `u8`, `usize` gibi; varsayılan `i32`. Taşma geliştirme derlemesinde paniğe yol açar.
- Ondalıklı `f64`; `0.1 + 0.2` tam `0.3` değildir.
- Sayılar kendiliğinden karışmaz; `as` açık dönüşümdür ve sessizce kesebilir.
- `bool` ve tek tırnaklı `char` tek değer, demet ve dizi sabit boyutlu birleşik türlerdir.
- Metin iki türlüdür: Sabit `&str` (`"Ada"`), değişebilen `String` (`String::from("Ada")`).
