# Hata Yönetimi

Dosya olmayabilir, kullanıcı sayı yerine harf yazabilir, ağ kopabilir. Programlar hata alır. Birçok dilde hata **istisna** (exception) olarak fırlatılır ve fonksiyonun imzasına bakınca hata verip vermeyeceğini göremezsin. Rust farklıdır: Olabilecek hata **dönüş türünde yazar.**

## İki tür hata

| Tür | Örnek | Rust'ta |
|---|---|---|
| **Kurtarılabilir** | Dosya yok, girdi bozuk | `Result` döndür |
| **Kurtarılamaz** | Programda bir hata, dizi sınırı aşıldı | `panic!` |

## Result

`Option` "değer var ya da yok" diyordu. `Result` "başarılı ya da hatalı" der:

```text
enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

`T` başarıda gelen değerin türü, `E` hatanın türü. `Option` gibi otomatik gelir. Bir sayıyı okuyalım:

```rust
fn main() {
    for text in ["42", "abc", ""] {
        match text.parse::<i32>() {
            Ok(n) => println!("number: {n}"),
            Err(e) => println!("error: {e}"),
        }
    }
}
```

```text
number: 42
error: invalid digit found in string
error: cannot parse integer from empty string
```

`parse` metni sayıya çevirmeyi dener. Hata türü `ParseIntError`, `{}` ile okunabilir bir mesaj yazar. `match` iki durumu da ele almayı zorunlu kılar.

## Kendi fonksiyonun

```rust
fn divide(a: i32, b: i32) -> Result<i32, String> {
    if b == 0 {
        return Err(String::from("division by zero"));
    }
    Ok(a / b)
}

fn main() {
    println!("{:?}", divide(10, 2));
    println!("{:?}", divide(1, 0));
}
```

```text
Ok(5)
Err("division by zero")
```

İmzaya bakan herkes bu fonksiyonun hata verebileceğini görüyor. Çağıran hatayı **görmezden gelemez**, çünkü `i32` değil `Result` elinde.

Görmezden gelmeye çalışırsan derleyici uyarır:

```rust
fn save() -> Result<(), String> {
    Ok(())
}

fn main() {
    save();
    println!("done");
}
```

```text
warning: unused `Result` that must be used
 --> main.rs:6:5
  |
6 |     save();
  |     ^^^^^^
  |
  = note: this `Result` may be an `Err` variant, which should be handled
  = note: `#[warn(unused_must_use)]` (part of `#[warn(unused)]`) on by default
help: use `let _ = ...` to ignore the resulting value
  |
6 |     let _ = save();
  |     +++++++
```

Bu bir uyarı, derleme durmaz, ama `#[must_use]` yazılı olduğu için derleyici görmezden geldiğini söyler.

## unwrap ve expect

`Option`'daki gibi: `Ok` ise değeri verir, `Err` ise panikler.

```rust
fn main() {
    let good: Result<i32, String> = Ok(3);
    println!("{}", good.unwrap());
    let bad: Result<i32, String> = Err(String::from("no value"));
    println!("{}", bad.expect("needed a value"));
}
```

```text
3

thread 'main' panicked at main.rs:5:24:
needed a value: "no value"
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

`expect` kendi mesajını başa ekler. Hangisini ne zaman?

| Yer | Yazım |
|---|---|
| Küçük deneme, örnek kod | `unwrap` |
| "Bu olamaz" diyebiliyorsan | `expect` ve nedenini yaz |
| Gerçekten olabilecek hata | `match`, `?` ya da `unwrap_or` |

## Varsayılan değerler

```rust
fn main() {
    println!("{}", "7".parse::<i32>().unwrap_or(0));
    println!("{}", "x".parse::<i32>().unwrap_or(0));
    println!("{}", "x".parse::<i32>().unwrap_or_default());
    println!("{}", "x".parse::<i32>().is_err());
}
```

```text
7
0
0
true
```

## ? işleci

Hatayı yukarı iletmek çok sık yapılır. `match` ile yazınca uzar:

```rust
fn add_text(a: &str, b: &str) -> Result<i32, std::num::ParseIntError> {
    let x = match a.parse::<i32>() {
        Ok(n) => n,
        Err(e) => return Err(e),
    };
    let y = match b.parse::<i32>() {
        Ok(n) => n,
        Err(e) => return Err(e),
    };
    Ok(x + y)
}

fn main() {
    println!("{:?}", add_text("2", "3"));
    println!("{:?}", add_text("2", "x"));
}
```

```text
Ok(5)
Err(ParseIntError { kind: InvalidDigit })
```

`?` aynı işi bir karakterle yapar:

```rust
fn add_text(a: &str, b: &str) -> Result<i32, std::num::ParseIntError> {
    let x = a.parse::<i32>()?;
    let y = b.parse::<i32>()?;
    Ok(x + y)
}

fn main() {
    println!("{:?}", add_text("2", "3"));
    println!("{:?}", add_text("2", "x"));
}
```

```text
Ok(5)
Err(ParseIntError { kind: InvalidDigit })
```

<figure class="fig"><div class="flow"><span class="node">a.parse()?</span><span class="arrow">→</span><span class="node ok">Ok ise değeri ver</span><span class="arrow">→</span><span class="node no">Err ise hemen dön</span></div><figcaption><code>?</code> ya değeri çıkarır ya da hatayı fonksiyondan döndürür.</figcaption></figure>

Birkaç `?` art arda yazılabilir ve kod "mutlu yolu" düz okunur.

## ? yalnızca Result döndüren fonksiyonda

```rust
fn main() {
    let n = "21".parse::<i32>()?;
    println!("{n}");
}
```

```text
error[E0277]: the `?` operator can only be used in a function that returns `Result` or
`Option` (or another type that implements `FromResidual`)
 --> main.rs:2:32
  |
1 | fn main() {
  | --------- this function should return `Result` or `Option` to accept `?`
2 |     let n = "21".parse::<i32>()?;
  |                                ^ cannot use the `?` operator in a function that
  returns `()`
  |
help: consider adding return type
  |
1 ~ fn main() -> Result<(), Box<dyn std::error::Error>> {
2 |     let n = "21".parse::<i32>()?;
3 |     println!("{n}");
4 +     Ok(())
  |
```

Fonksiyon `Result` döndürmüyorsa hatayı nereye döndürsün? `main` de `Result` döndürebilir:

```rust
fn main() -> Result<(), std::num::ParseIntError> {
    let n = "21".parse::<i32>()?;
    println!("{}", n * 2);
    Ok(())
}
```

```text
42
```

`main` `Err` dönerse program hatayı yazar ve 1 ile çıkar:

```rust
fn main() -> Result<(), String> {
    println!("start");
    Err(String::from("config is missing"))
}
```

```text
start
Error: "config is missing"
```

## Hatanın türü farklıysa

`?` hata türlerinin uyuşmasını ister:

```rust
fn read(text: &str) -> Result<i32, String> {
    let n = text.parse::<i32>()?;
    Ok(n)
}

fn main() {
    println!("{:?}", read("1"));
}
```

```text
error[E0277]: `?` couldn't convert the error to `String`
 --> main.rs:2:32
  |
1 | fn read(text: &str) -> Result<i32, String> {
  |                        ------------------- expected `String` because of this
2 |     let n = text.parse::<i32>()?;
  |                  --------------^ the trait `From<ParseIntError>` is not implemented
  for `String`
  |                  |
  |                  this can't be annotated with `?` because it has type `Result<_,
  ParseIntError>`
  |
  = note: the question mark operation (`?`) implicitly performs a conversion on the
    error value using the `From` trait
  = help: `String` implements trait `From<T>`:
            From<&String>
            From<&mut str>
            From<&str>
            From<Box<str>>
            From<Cow<'_, str>>
            From<char>
```

Şimdilik en basit yol `map_err`: Hatayı bizim türümüze çevirir. Parantez içindeki `|e| ...` adsız, tek satırlık bir fonksiyondur:

```rust
fn double(text: &str) -> Result<i32, String> {
    let n = text.parse::<i32>().map_err(|e| format!("bad number {text:?}: {e}"))?;
    Ok(n * 2)
}

fn main() {
    println!("{:?}", double("4"));
    println!("{:?}", double("x"));
}
```

```text
Ok(8)
Err("bad number \"x\": invalid digit found in string")
```

## Kendi hata türün

`String` hata yetiyor ama çağıran hatanın türüne göre davranamaz. Enum tam bunun içindir:

```rust
#[derive(Debug)]
enum AgeError {
    NotANumber,
    OutOfRange(i32),
}

fn read_age(text: &str) -> Result<i32, AgeError> {
    let age = text.parse::<i32>().map_err(|_| AgeError::NotANumber)?;
    if age < 0 || age > 150 {
        return Err(AgeError::OutOfRange(age));
    }
    Ok(age)
}

fn main() {
    for text in ["36", "x", "200"] {
        match read_age(text) {
            Ok(age) => println!("age {age}"),
            Err(AgeError::NotANumber) => println!("not a number"),
            Err(AgeError::OutOfRange(n)) => println!("{n} is out of range"),
        }
    }
}
```

```text
age 36
not a number
200 is out of range
```

Çağıran artık `match` ile her hatayı ayrı ele alabilir ve yeni bir hata türü eklendiğinde derleyici eksik dalı gösterir. Sonraki modülde bu türü `Display` ve `Error` özellikleriyle tamamlayacağız.

## Option ile Result arasında

```rust
fn first_char(text: &str) -> Result<char, String> {
    text.chars().next().ok_or(String::from("empty"))
}

fn first_number(list: &[&str]) -> Option<i32> {
    let text = list.first()?;
    text.parse().ok()
}

fn main() {
    println!("{:?} {:?}", first_char("hi"), first_char(""));
    println!("{:?}", first_number(&["7"]));
    println!("{:?} {:?}", first_number(&["x"]), first_number(&[]));
}
```

```text
Ok('h') Err("empty")
Some(7)
None None
```

`ok_or` `Option`'ı `Result`'a, `.ok()` `Result`'ı `Option`'a çevirir. `?` `Option` döndüren fonksiyonda `Option` üzerinde de çalışır.

## panic! ne zaman?

`panic!` programı durdurur. Kişinin girdisi yüzünden değil, **programda bir hata olduğunda** kullanılır:

```rust
fn main() {
    let level = 9;
    if level > 5 {
        panic!("level must be at most 5, got {level}");
    }
}
```

```text
thread 'main' panicked at main.rs:4:9:
level must be at most 5, got 9
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

Bu çıktı stderr'e gider, program 101 ile çıkar. Kural: Sorun çağıranın düzeltebileceği bir şeyse `Result`, kodun kendi hatasıysa `panic!`.

## Özet

- Olabilecek hata dönüş türünde yazar: `Result<T, E>`.
- `Ok(deger)` ve `Err(hata)` iki durumdur. `match` ikisini de ister.
- `unwrap` ve `expect` `Err`'de panikler; gerçek hatada kullanma.
- `?` hatayı yukarı iletir; yalnızca `Result` (ya da `Option`) döndüren fonksiyonda çalışır.
- Tür uymuyorsa `map_err`. Çağıran ayırt edecekse enum hata türü.
- `panic!` yalnızca programın kendi hatası için.
