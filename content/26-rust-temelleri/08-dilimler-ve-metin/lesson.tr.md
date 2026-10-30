# Dilimler, String ve &str

Rust'ta metin için iki tür görüyoruz ve başlarda en kafa karıştıran konulardan biri bu. Sahiplik ile ödünç almayı bildiğin için artık açıklaması kolay.

## Dilim: Bir parçayı ödünç almak

**Dilim** (slice) bir verinin bir parçasına bakan referanstır. Sahip değildir, yalnızca başlangıç adresi ve uzunluk tutar. Önce sayılarla görelim:

```rust
fn main() {
    let days = [10, 20, 30, 40, 50];
    let middle = &days[1..4];
    println!("{:?}", middle);
    println!("{:?}", &days[..2]);
    println!("{:?}", &days[3..]);
    println!("{}", middle.len());
}
```

```text
[20, 30, 40]
[10, 20]
[40, 50]
3
```

`&days[1..4]` 1, 2, 3 sıralı elemanları gösterir. Türü `&[i32]`: "`i32` dilimi". Başı ya da sonu yazmayabilirsin: `[..2]` baştan, `[2..]` sona kadar, `[..]` tamamı.

Dilim veriyi kopyalamaz. Hangi uzunlukta dizi gelirse gelsin çalışan fonksiyonlar bu sayede yazılır:

```rust
fn total(values: &[i32]) -> i32 {
    let mut sum = 0;
    for v in values {
        sum += v;
    }
    sum
}

fn main() {
    let short = [1, 2];
    let long = [1, 2, 3, 4, 5];
    println!("{}", total(&short));
    println!("{}", total(&long));
    println!("{}", total(&long[1..3]));
}
```

```text
3
15
5
```

`[i32; 4]` boyutu türün parçası olan bir diziydi. `&[i32]` ise boyutu çalışırken bilinen bir görünüm.

## &str: Metin dilimi

`&str` bir metnin parçasına bakan dilimdir. İki sayıdan oluşur: adres ve uzunluk.

```rust
fn main() {
    let text = String::from("hello world");
    let first = &text[0..5];
    let second = &text[6..];
    println!("{first} / {second}");
}
```

```text
hello / world
```

<figure class="fig"><svg viewBox="0 0 640 168" width="640" xmlns="http://www.w3.org/2000/svg"><text class="dim" x="20" y="24" font-size="13" font-weight="600">yığın (stack)</text><text class="dim" x="390" y="24" font-size="13" font-weight="600">öbek (heap)</text><g><rect class="box" x="20" y="44" width="230" height="44" rx="8"/><text class="ink" x="34" y="71" font-size="14" font-weight="600">text</text><text class="dim" x="110" y="71" font-size="12.5">ptr, len 11, cap 11</text></g><g><rect class="box" x="20" y="102" width="230" height="44" rx="8"/><text class="ink" x="34" y="129" font-size="14" font-weight="600">first</text><text class="dim" x="110" y="129" font-size="12.5">ptr, len 5</text></g><g><rect class="box" x="390" y="44" width="220" height="44" rx="8"/><text class="ink" x="404" y="71" font-size="14">hello world</text></g><path class="curve" d="M250 66 C320 66 320 66 382 66"/><polygon class="dot" points="390,66 380,61 380,71"/><path class="curve" d="M250 124 C320 124 320 66 382 66"/><polygon class="dot" points="390,66 380,61 380,71"/></svg><figcaption><code>first</code> aynı metnin başını gösterir ve uzunluk olarak 5 tutar; kopya yoktur, kapasite de yoktur.</figcaption></figure>

Kodun içine yazdığın `"hello"` da `&str`'dir: Metin programın içine gömülür ve onu gösteren bir dilim alırsın. Bu yüzden değiştirilemez. Tam adı `&'static str`:
`'static` "program boyunca yaşar" demektir.

## String ve &str

<figure class="fig"><div class="versus"><div><h4>String</h4>Sahiptir. Öbekte durur, büyüyebilir, değiştirilebilir. Kapsam bitince silinir.</div><div><h4>&amp;str</h4>Ödünç alır. Bir metnin parçasına bakar, değiştiremez. Çok ucuzdur.</div></div><figcaption>Aynı ilişki <code>Vec&lt;T&gt;</code> ile <code>&amp;[T]</code> arasında da var.</figcaption></figure>

Aradaki dönüşümler:

```rust
fn main() {
    let borrowed: &str = "hi";
    let owned: String = borrowed.to_string();
    let again: &str = &owned;
    let copy: String = String::from(again);
    println!("{borrowed} {owned} {again} {copy}");
}
```

```text
hi hi hi hi
```

## Fonksiyonlar &str almalı

Önceki bölümde `&String` yazmıştık. Daha iyisi `&str`: Hem `String` hem metin sabiti kabul eder.

```rust
fn shout(text: &str) -> String {
    text.to_uppercase()
}

fn main() {
    let text = String::from("owned");
    println!("{}", shout(&text));
    println!("{}", shout("constant"));
    println!("{}", shout(&text[..2]));
}
```

```text
OWNED
CONSTANT
OW
```

`&text` bir `&String`'dir ama Rust onu kendiliğinden `&str`'ye çevirir. Buna **deref zorlaması** (deref coercion) denir. Clippy aracı `&String` parametresinde seni uyarır.
Aynı şekilde `&Vec<T>` yerine `&[T]` yazılır.

## Dilimler güvenlidir

Bir metnin ilk kelimesini döndüren fonksiyon yazalım. Metin sonra temizlenirse, sayı döndürseydik sayı anlamsız kalırdı. Dilim döndürürsek derleyici bizi korur:

```rust
fn first_word(text: &str) -> &str {
    match text.find(' ') {
        Some(position) => &text[..position],
        None => text,
    }
}

fn main() {
    let mut text = String::from("hello world");
    let word = first_word(&text);
    text.clear();
    println!("{word}");
}
```

```text
error[E0502]: cannot borrow `text` as mutable because it is also borrowed as immutable
  --> main.rs:11:5
   |
10 |     let word = first_word(&text);
   |                           ----- immutable borrow occurs here
11 |     text.clear();
   |     ^^^^^^^^^^^^ mutable borrow occurs here
12 |     println!("{word}");
   |                ---- immutable borrow later used here
```

Dilim `text`'i ödünç aldı, bu yüzden `clear` çağrısı `E0502` veriyor. Hata çalışırken değil, derlerken yakalandı.

## En önemli tuzak: Metin UTF-8'dir

Bilgisayarda metin **UTF-8** ile bayt olarak tutulur. İngilizce harfler 1 bayt, ama Türkçedeki `ş`, `ğ`, `ı` gibi harfler 2 bayttır. `.len()` harf sayısını değil **bayt** sayısını verir:

```rust
fn main() {
    println!("{}", "kitap".len());
    println!("{}", "şeker".len());
    println!("{}", "şeker".chars().count());
}
```

```text
5
6
5
```

Bu yüzden Rust metne `text[0]` ile ulaşmaya izin vermez. "0. eleman" bir harfin yarısı olabilirdi:

```rust
fn main() {
    let text = String::from("hello");
    println!("{}", text[0]);
}
```

```text
error[E0277]: the type `str` cannot be indexed by `{integer}`
 --> main.rs:3:25
  |
3 |     println!("{}", text[0]);
  |                         ^ string indices are ranges of `usize`
  |
  = help: the trait `SliceIndex<str>` is not implemented for `{integer}`
  = note: you can use `.chars().nth()` or `.bytes().nth()`
          for more information, see chapter 8 in The Book:
          <https://doc.rust-lang.org/book/ch08-02-strings.html#indexing-into-strings>
help: `usize` implements trait `SliceIndex<T>`
 -->
 /rustc/58cf8f9c35b355199727627d07ae34a4e2846d67/library\core\src\slice\index.rs:179:0
  |
  = note: `SliceIndex<[T]>`
 -->
 /rustc/58cf8f9c35b355199727627d07ae34a4e2846d67/library\core\src\bstr\traits.rs:197:0
  |
  = note: `SliceIndex<ByteStr>`
  = note: required for `String` to implement `Index<{integer}>`
```

Dilim alırken sınır bir harfin ortasına denk gelirse program panikler:

```rust
fn main() {
    let text = String::from("şeker");
    println!("{}", &text[0..1]);
}
```

```text
thread 'main' panicked at main.rs:3:25:
end byte index 1 is not a char boundary; it is inside 'ş' (bytes 0..2 of string)
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

`ş` harfi 0 ve 1. baytları tutuyor, `[0..1]` onu ikiye bölerdi. Harf harf çalışmak için `.chars()` kullanılır:

```rust
fn main() {
    let word = "şeker";
    for letter in word.chars() {
        print!("[{letter}]");
    }
    println!();
    let reversed: String = word.chars().rev().collect();
    println!("{reversed}");
    println!("{}", word.chars().count());
}
```

```text
[ş][e][k][e][r]
rekeş
5
```

`.chars().rev()` ters çevirir, `.collect()` parçaları yeni bir `String`'de toplar. `.count()` gerçek harf sayısını verir. Satır sonu gibi şeyler için `.lines()`, kelimeler için `.split_whitespace()` var.

## Sık kullanılan metin metotları

```rust
fn main() {
    let line = "  Rust is fun  ";
    println!("[{}]", line.trim());
    println!("{}", line.to_uppercase().trim());
    println!("{}", line.contains("fun"));
    println!("{}", line.trim().starts_with("Rust"));
    println!("{}", line.trim().replace("fun", "hard"));
    for word in line.split_whitespace() {
        println!("{word}");
    }
}
```

```text
[Rust is fun]
RUST IS FUN
true
true
Rust is hard
Rust
is
fun
```

| Metot | Ne yapar | Döner |
|---|---|---|
| `trim` | Baştaki ve sondaki boşluğu atar | `&str` |
| `to_uppercase` | Büyük harfe çevirir | `String` |
| `contains` | İçinde var mı | `bool` |
| `starts_with` | Böyle mi başlıyor | `bool` |
| `replace` | Değiştirir | `String` |
| `split` | Bölerek gezer | iterator |

Bir kural fark ettin mi? **Yeni metin üretenler `String`, var olana bakanlar `&str` döndürür.** `trim` bellek ayırmaz, aynı metnin bir parçasını gösterir.

## Metin birleştirmek

```rust
fn main() {
    let a = String::from("Hello");
    let b = String::from("World");
    let with_format = format!("{a}, {b}!");
    println!("{with_format}");
    let with_plus = a + ", " + &b;
    println!("{with_plus}");
    println!("{b}");
}
```

```text
Hello, World!
Hello, World
World
```

`format!` en okunaklı yoldur ve hiçbir şeyi taşımaz. `+` soldaki `String`'i taşır, bu yüzden `a` sonra kullanılamaz.

## Özet

- Dilim, verinin bir parçasına bakan referanstır: `&[T]` ya da `&str`.
- `String` sahiptir ve büyür; `&str` ödünç alır. Fonksiyon parametresinde `&str`, `&[T]` tercih edilir.
- `.len()` bayt sayısıdır. Türkçe harfler 2 bayttır. `text[0]` derlenmez, harf ortasından dilim panikler.
- Harf harf çalışmak için `.chars()`.
- Yeni metin üreten metotlar `String`, bakanlar `&str` döndürür.
