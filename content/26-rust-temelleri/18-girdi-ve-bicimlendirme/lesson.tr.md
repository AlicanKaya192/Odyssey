# Girdi ve Biçimlendirme

Şimdiye kadar bütün değerler kodun içindeydi. Gerçek bir program dışarıdan veri alır ve sonucu okunur biçimde
yazar. Bu bölümde ikisini de öğreniyoruz: Kullanıcıdan bir satır okumak, onu sayıya çevirmek ve çıktıyı hizalı,
istediğin kadar basamakla yazmak.

## Bir satır okumak

```rust
use std::io;

fn main() {
    let mut line = String::new();
    io::stdin().read_line(&mut line).expect("could not read");
    println!("You wrote: {line}");
}
```

Girdi:

```text
Ada
```

Çıktı:

```text
You wrote: Ada
```

Bu kodda yeni çok şey var. Hepsini şimdi anlaman gerekmiyor, çoğu ileride kendi bölümünde geliyor. Şimdilik
bu satırları **kalıp** olarak yaz:

<figure class="fig"><div class="anat"><div class="anat-row"><span><code>use std::io;</code></span><span>Girdi ve çıktı araçlarını <code>io</code> adıyla kullanacağım.</span></div><div class="anat-row"><span><code>String::new()</code></span><span>Büyüyebilen boş bir metin açar.</span></div><div class="anat-row"><span><code>io::stdin()</code></span><span><b>Standart girdi</b> (stdin): programa dışarıdan gelen veri, çoğunlukla klavye.</span></div><div class="anat-row"><span><code>.read_line(&amp;mut line)</code></span><span>Bir satır okur ve <code>line</code> metninin sonuna ekler. <code>&amp;mut</code> "bunu değiştirebilirsin" demektir, Ödünç Alma bölümünde göreceğiz.</span></div><div class="anat-row"><span><code>.expect("...")</code></span><span>Okuma başarısız olursa programı bu mesajla durdurur.</span></div></div><figcaption>Girdi okuma kalıbının parçaları.</figcaption></figure>

Odyssey'de girdi isteyen alıştırmalarda hazır girdiyi denetleyici verir; senin yazmanı beklemez. Kendi bilgisayarında
çalıştırırsan program satır yazmanı bekler.

## Görünmeyen satır sonu

`line` metninde gözle görülmeyen bir şey daha var: Enter'a basmak da girdinin parçasıdır ve metnin içine girer.
`{:?}` biçimi metni tırnak içinde, görünmeyen karakterleri de göstererek yazar:

```rust
use std::io;

fn main() {
    let mut line = String::new();
    io::stdin().read_line(&mut line).expect("could not read");
    println!("{line:?}");
}
```

```text
"Ada\r\n"
```

`\r\n` Windows'taki satır sonudur (Linux ve macOS'ta yalnızca `\n`). `trim` baştaki ve sondaki boşlukları ve satır sonunu
atar. Ortadaki boşluklara dokunmaz:

```rust
use std::io;

fn main() {
    let mut line = String::new();
    io::stdin().read_line(&mut line).expect("could not read");
    let name = line.trim();
    println!("Hello, {name}!");
}
```

```text
Hello, Ada!
```

Burada girdi `  Ada  ` idi.

## Metinden sayıya: `parse`

`read_line` her zaman metin verir. `41` yazılsa da elimizde `"41\r\n"` metni vardır, onunla toplama yapılmaz. `parse`
metni sayıya çevirmeyi dener:

```rust
use std::io;

fn main() {
    let mut line = String::new();
    io::stdin().read_line(&mut line).expect("could not read");
    let age: i32 = line.trim().parse().expect("not a number");
    println!("{}", age + 1);
}
```

```text
42
```

İki şeye dikkat et. `: i32` hangi türe çevrileceğini söylüyor; yazmazsan derleyici sorar:

```rust
use std::io;

fn main() {
    let mut line = String::new();
    io::stdin().read_line(&mut line).expect("could not read");
    let age = line.trim().parse().expect("not a number");
    println!("{age}");
}
```

```text
error[E0284]: type annotations needed
 --> main.rs:6:9
  |
6 |     let age = line.trim().parse().expect("not a number");
  |         ^^^               ----- type must be known at this point
  |
  = note: cannot satisfy `<_ as FromStr>::Err == _`
  = note: the type must also implement `FromStr`
note: required by a bound in `core::str::<impl str>::parse`
help: consider giving `age` an explicit type
  |
6 |     let age: /* Type */ = line.trim().parse().expect("not a number");
  |            ++++++++++++
```

İkincisi `trim`. Satır sonu rakam olmadığı için onsuz çevirme başarısız olur ve `expect` programı durdurur:

```rust
use std::io;

fn main() {
    let mut line = String::new();
    io::stdin().read_line(&mut line).expect("could not read");
    let age: i32 = line.parse().expect("not a number");
    println!("{}", age + 1);
}
```

```text
thread 'main' panicked at main.rs:6:33:
not a number: ParseIntError { kind: InvalidDigit }
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

Kullanıcı `abc` yazarsa da aynı şey olur. Şimdilik durmak yeterli; hatayı nazikçe ele almayı Hata Yönetimi bölümünde
öğreneceğiz.

## Soruyu aynı satırda sormak

`println!` sonuna satır sonu ekler, `print!` eklemez. Ama `print!`'in yazısı satır sonu gelene kadar bekleyebilir, soru
ekranda görünmeden program girdi beklemeye başlar. `flush` bekleyeni hemen gönderir:

```rust
use std::io::{self, Write};

fn main() {
    print!("What is your name? ");
    io::stdout().flush().expect("could not write");

    let mut line = String::new();
    io::stdin().read_line(&mut line).expect("could not read");
    println!("Hello, {}!", line.trim());
}
```

Girdi `Ada` iken:

```text
What is your name? Hello, Ada!
```

Kendi terminalinde yazdığın ad da aynı satırda görünür ve Enter'dan sonra yeni satıra geçilir. Burada girdi yönlendirildiği
için yazdığın yer görünmüyor. `use std::io::{self, Write};`, `flush` için `Write`'ı da getiriyor.

## İki satır okumak: `clear` tuzağı

`read_line` metnin **üzerine yazmaz, sonuna ekler**. Aynı metinle iki kez okursan iki satır yan yana durur:

```rust
use std::io;

fn main() {
    let mut line = String::new();
    io::stdin().read_line(&mut line).expect("could not read");
    io::stdin().read_line(&mut line).expect("could not read");
    println!("{line:?}");
}
```

Girdi `3` ve `4` iken:

```text
"3\r\n4\r\n"
```

Bu metin sayıya çevrilemez. İkinci okumadan önce metni boşalt:

```rust
use std::io;

fn main() {
    let mut line = String::new();
    io::stdin().read_line(&mut line).expect("could not read");
    let a: i32 = line.trim().parse().expect("not a number");

    line.clear();
    io::stdin().read_line(&mut line).expect("could not read");
    let b: i32 = line.trim().parse().expect("not a number");

    println!("{}", a + b);
}
```

```text
7
```

## Değeri yerine koymak

`println!`, `format!` ve benzerleri aynı biçim dilini kullanır. Süslü parantez değerin yeridir:

```rust
fn main() {
    let name = "Ada";
    let age = 36;
    println!("{} is {}", name, age);
    println!("{name} is {age}");
    println!("{0} and {1} and {0}", name, age);
    println!("{who} is {}", age + 1, who = name);
}
```

```text
Ada is 36
Ada is 36
Ada and 36 and Ada
Ada is 37
```

Süslü parantezin içine ad yazmak en okunur olanıdır. Ama yalnızca düz değişken adı yazılabilir: `{age + 1}` olmaz, hesap
virgülden sonra verilir.

## Ondalık basamak

`:` işaretinden sonrası biçimi söyler. `.2`, noktadan sonra 2 basamak demektir:

```rust
fn main() {
    let pi = 3.14159;
    println!("{pi:.2}");
    println!("{:.0}", pi);
    println!("{:.3}", 2.0);
    println!("{:.0}", 2.5);
    println!("{:.0}", 3.5);
}
```

```text
3.14
3
2.000
2
4
```

Sayıyı değiştirmez, yalnızca yazılışını değiştirir. Son iki satıra dikkat: `2.5` değeri `2`, `3.5` değeri `4` oldu. Tam
ortadaki değer çift olan komşuya yuvarlanır, her zaman yukarı değil.

## Genişlik ve hizalama

Sütun yazarken her değere sabit bir genişlik verilir. Köşeli parantezleri kenarları görelim diye koyduk:

```rust
fn main() {
    println!("[{:5}]", 42);
    println!("[{:5}]", "ab");
    println!("[{:>5}]", "ab");
    println!("[{:<5}]", 42);
    println!("[{:^5}]", "ab");
    println!("[{:*^7}]", "ab");
    println!("[{:05}]", 42);
    println!("[{:+}]", 42);
}
```

```text
[   42]
[ab   ]
[   ab]
[42   ]
[ ab  ]
[**ab***]
[00042]
[+42]
```

| Biçim | Anlamı |
|---|---|
| `{:5}` | 5 karakter; sayı sağa, metin sola yaslanır |
| `{:>5}` | Sağa yasla |
| `{:<5}` | Sola yasla |
| `{:^5}` | Ortala; eşit bölünmezse fazlası sağa |
| `{:*^7}` | Boşluk yerine `*` doldur |
| `{:05}` | Boşluk yerine sıfır doldur |
| `{:+}` | Artı işaretini de yaz |

Bunları birleştirince tablo olur. `{:>8.2}`: 8 genişlikte, sağa yaslı, 2 basamak:

```rust
fn main() {
    println!("{:<8}{:>4}{:>8}", "item", "qty", "price");
    println!("{:<8}{:>4}{:>8.2}", "tea", 2, 3.5);
    println!("{:<8}{:>4}{:>8.2}", "coffee", 1, 12.25);
}
```

```text
item     qty   price
tea        2    3.50
coffee     1   12.25
```

## Başka gösterimler

Aynı sayıyı başka tabanda yazabilirsin. `{:?}` ise geliştiriciye yönelik gösterimdir: Metni tırnakla yazar, demet gibi `{}`
kabul etmeyen türleri de yazar. `{:#?}` aynısını çok satırlı yapar.

```rust
fn main() {
    println!("{:b}", 10);
    println!("{:o}", 10);
    println!("{:x}", 255);
    println!("{:X}", 255);
    println!("{:#x}", 255);
    println!("{:08b}", 10);
    println!("{:e}", 1500.0);
}
```

```text
1010
12
ff
FF
0xff
00001010
1.5e3
```

```rust
fn main() {
    let name = "Ada";
    println!("{name}");
    println!("{name:?}");
    let point = (3, "north");
    println!("{point:?}");
    println!("{point:#?}");
}
```

```text
Ada
"Ada"
(3, "north")
(
    3,
    "north",
)
```

## Biçimi metne yazmak

`format!`, `println!` gibi yazılır ama ekrana basmak yerine `String` verir. Süslü parantezin kendisini yazmak için iki kez
yazılır:

```rust
fn main() {
    let price = 12.5;
    let label = format!("{price:.2} TL");
    println!("{label}");
    println!("{}", label.len());
    println!("{{not a placeholder}}");
}
```

```text
12.50 TL
8
{not a placeholder}
```

## Özet

- Satır okuma kalıbı: `String::new()`, `io::stdin().read_line(&mut line).expect("...")`.
- Okunan metnin sonunda satır sonu vardır; `trim` atar. `{:?}` görünmeyeni gösterir.
- `line.trim().parse()` sayıya çevirir; hedef tür `: i32` ile söylenir, başarısız olabilir.
- `read_line` sonuna ekler: Yeniden okumadan önce `line.clear()`.
- `{:.2}` basamak, `{:>5}` hizalama ve genişlik, `{:05}` sıfır doldurma; birlikte `{:>8.2}`.
- `format!` aynı biçimle `String` üretir; `{:?}` ve `{:#?}` geliştirici gösterimidir.
