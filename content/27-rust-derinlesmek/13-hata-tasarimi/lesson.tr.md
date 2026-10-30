# Hata Tasarımı

Temeller'de `Result` ve `?` işlecini öğrendik. Şimdi soru başka: **Hatanın türü ne olmalı?** Hata tek bir `String` olursa çağıran kod hatayı yalnızca ekrana yazabilir. Ne olduğuna bakıp karar veremez. İyi tasarlanmış hata türü, çağırana seçim hakkı verir.

## Hata bir enum'dır

Olabilecek hataları tek tek yaz. İki trait onu gerçek bir hata yapar:

- `Display`: İnsanın okuyacağı metin.
- `std::error::Error`: "Bu tür bir hatadır" der. Gövdesi boş olabilir, çünkü `Debug` ve `Display` istiyor, gerisinin hazır hâli var.

```rust
use std::fmt;

#[derive(Debug)]
enum AgeError {
    Empty,
    TooBig(u32),
}

impl fmt::Display for AgeError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            AgeError::Empty => write!(f, "age is empty"),
            AgeError::TooBig(n) => write!(f, "age {n} is too big"),
        }
    }
}

impl std::error::Error for AgeError {}

fn check(age: Option<u32>) -> Result<u32, AgeError> {
    let age = age.ok_or(AgeError::Empty)?;
    if age > 150 {
        return Err(AgeError::TooBig(age));
    }
    Ok(age)
}

fn main() {
    println!("{:?}", check(Some(30)));
    for input in [None, Some(200)] {
        if let Err(e) = check(input) {
            println!("{e} / {e:?}");
        }
    }
}
```

```text
Ok(30)
age is empty / Empty
age 200 is too big / TooBig(200)
```

`{e}` kullanıcı içindir, `{e:?}` geliştirici için. Hata türü olduğu için çağıran `match` ile her durumu ayrı ele alabilir.

## `?` ve From

`?` hatayı olduğu gibi döndürmez, önce `From` ile dönüştürür. Dönüşüm yazılmamışsa:

```rust
use std::num::ParseIntError;

#[derive(Debug)]
enum AppError {
    Parse(ParseIntError),
    Negative(i64),
}

fn read_age(text: &str) -> Result<i64, AppError> {
    let n = text.trim().parse::<i64>()?;
    if n < 0 {
        return Err(AppError::Negative(n));
    }
    Ok(n)
}

fn main() {
    println!("{:?}", read_age("30"));
    println!("{:?}", read_age("x"));
    println!("{:?}", read_age("-1"));
}
```

```text
error[E0277]: `?` couldn't convert the error to `AppError`
  --> main.rs:10:39
   |
 9 | fn read_age(text: &str) -> Result<i64, AppError> {
   |                            --------------------- expected `AppError` because of
   this
10 |     let n = text.trim().parse::<i64>()?;
   |                         --------------^ the trait `From<ParseIntError>` is not
   implemented for `AppError`
   |                         |
   |                         this can't be annotated with `?` because it has type
   `Result<_, ParseIntError>`
   |
note: `AppError` needs to implement `From<ParseIntError>`
  --> main.rs:4:1
   |
 4 | enum AppError {
   | ^^^^^^^^^^^^^
   = note: the question mark operation (`?`) implicitly performs a conversion on the
     error value using the `From` trait
```

Derleyici tam olarak bunu söylüyor: `?`, `ParseIntError`'ı `AppError`'a çeviremiyor. `From` yazınca her `?` kendiliğinden çevirir:

```rust
use std::num::ParseIntError;

#[derive(Debug)]
enum AppError {
    Parse(ParseIntError),
    Negative(i64),
}

impl From<ParseIntError> for AppError {
    fn from(e: ParseIntError) -> Self {
        AppError::Parse(e)
    }
}

fn read_age(text: &str) -> Result<i64, AppError> {
    let n = text.trim().parse::<i64>()?;
    if n < 0 {
        return Err(AppError::Negative(n));
    }
    Ok(n)
}

fn main() {
    println!("{:?}", read_age("30"));
    println!("{:?}", read_age("x"));
    println!("{:?}", read_age("-1"));
}
```

```text
Ok(30)
Err(Parse(ParseIntError { kind: InvalidDigit }))
Err(Negative(-1))
```

Fonksiyonun gövdesinde hiç dönüşüm yazılı değil. `map_err` kalabalığı böyle biter.

## Hatanın sebebi

Bir hata başka bir hatadan doğar: "port okunamadı" çünkü "sayı çok büyük". `Error` trait'inin `source` yöntemi bu zinciri kurar. Yukarıdaki katman **bağlamı** ekler, alttaki **sebebi** saklar:

```rust
use std::error::Error;
use std::fmt;
use std::num::ParseIntError;

#[derive(Debug)]
struct ConfigError {
    key: String,
    source: ParseIntError,
}

impl fmt::Display for ConfigError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "bad value for {}", self.key)
    }
}

impl Error for ConfigError {
    fn source(&self) -> Option<&(dyn Error + 'static)> {
        Some(&self.source)
    }
}

fn read_port(text: &str) -> Result<u16, ConfigError> {
    text.parse::<u16>().map_err(|e| ConfigError {
        key: String::from("port"),
        source: e,
    })
}

fn report(err: &dyn Error) {
    println!("error: {err}");
    let mut current = err.source();
    while let Some(cause) = current {
        println!("caused by: {cause}");
        current = cause.source();
    }
}

fn main() {
    if let Err(e) = read_port("99999") {
        report(&e);
    }
}
```

```text
error: bad value for port
caused by: number too large to fit in target type
```

`source` içindeki `dyn Error + 'static` yazımı korkutmasın: "herhangi bir hata" demek. Zinciri gezen `report` fonksiyonu hangi hata türüyle olursa olsun çalışır, çünkü yalnızca trait'i biliyor.

Tek kural: Sebep ile metni çift yazma. `Display` kendi cümlesini söyler, sebebi `source` taşır. İkisi birden aynı şeyi yazarsa zincir basılınca metin iki kez görünür.

## Kısa ad

Her fonksiyonda aynı hata türü yazılıyorsa kısa bir ad tanımla. Standart kütüphane de böyle yapar (`std::io::Result`, `fmt::Result`):

```rust
#[derive(Debug)]
enum AppError {
    Empty,
}

type Result<T> = std::result::Result<T, AppError>;

fn first(list: &[i32]) -> Result<i32> {
    list.first().copied().ok_or(AppError::Empty)
}

fn main() {
    println!("{:?}", first(&[4, 5]));
    println!("{:?}", first(&[]));
}
```

```text
Ok(4)
Err(Empty)
```

## Box&lt;dyn Error&gt;: Her hatayı alan kutu

Küçük bir araçta enum yazmak fazla gelebilir. `Box<dyn Error>` her hata türünü alır, `?` çevirmeyi kendisi yapar. Üstelik düz metin de `.into()` ile hataya dönüşür:

```rust
use std::error::Error;

fn sum_line(text: &str) -> Result<i32, Box<dyn Error>> {
    if text.is_empty() {
        return Err("empty line".into());
    }
    let mut total = 0;
    for part in text.split(',') {
        total += part.trim().parse::<i32>()?;
    }
    Ok(total)
}

fn main() {
    for line in ["1, 2", "", "1, x"] {
        match sum_line(line) {
            Ok(n) => println!("{n}"),
            Err(e) => println!("error: {e}"),
        }
    }
}
```

```text
3
error: empty line
error: invalid digit found in string
```

Bedeli: Çağıran artık ne olduğunu bilmiyor, yalnızca metnini yazabiliyor. Gerçekten bakmak gerekirse `downcast_ref` türü çalışma anında sorar:

```rust
use std::num::ParseIntError;

fn main() {
    let err = sum_line("x").unwrap_err();
    if let Some(p) = err.downcast_ref::<ParseIntError>() {
        println!("number problem: {p}");
    }
    println!("{}", err.is::<std::fmt::Error>());
}
```

```text
number problem: invalid digit found in string
false
```

`downcast_ref` işe yarıyorsa hata türünü enum yapmanın zamanı gelmiştir.

## Hangisi?

| Yazdığın | Seç | Neden |
|---|---|---|
| Kütüphane | Kendi enum'un | Çağıran duruma göre karar verir |
| Uygulama, küçük araç | `Box<dyn Error>` | Hata en sonunda ekrana yazılır |
| Uygulamada kurtarılacak hata | Enum | `match` ile yeniden dene, varsayılana dön |

## main'den hata dönmek

`main` de `Result` döndürebilir. Sorun şu: Hatayı `Debug` ile yazar, `Display` ile değil.

```rust
use std::error::Error;

fn main() -> Result<(), Box<dyn Error>> {
    let n: i32 = "x".parse()?;
    println!("{n}");
    Ok(())
}
```

```text
Error: ParseIntError { kind: InvalidDigit }
```

Kullanıcıya bunu göstermek istemeyiz. Asıl işi `run` adlı bir fonksiyona koy; `main` hatayı düzgün yazıp çıkış kodunu seçsin:

```rust
use std::num::ParseIntError;
use std::process::ExitCode;

fn run() -> Result<i32, ParseIntError> {
    "x".parse()
}

fn main() -> ExitCode {
    match run() {
        Ok(n) => {
            println!("{n}");
            ExitCode::SUCCESS
        }
        Err(e) => {
            eprintln!("error: {e}");
            ExitCode::from(2)
        }
    }
}
```

```text
error: invalid digit found in string
```

## Birçok Result

Bir listeyi çevirirken her biri `Result` üretir. `collect` bunları ilk hatada durarak tek `Result`'a toplayabilir; bütün hataları görmek için `partition`:

```rust
fn main() {
    let good: Result<Vec<i32>, _> = ["1", "2"].iter().map(|s| s.parse::<i32>()).collect();
    let bad: Result<Vec<i32>, _> = ["1", "x"].iter().map(|s| s.parse::<i32>()).collect();
    println!("{good:?}");
    println!("{bad:?}");

    let (ok, err): (Vec<_>, Vec<_>) = ["1", "x", "3"]
        .iter()
        .map(|s| s.parse::<i32>())
        .partition(|r| r.is_ok());
    println!("{} {}", ok.len(), err.len());
}
```

```text
Ok([1, 2])
Err(ParseIntError { kind: InvalidDigit })
2 1
```

## Özet

- Hata enum'dır: `Debug`, `Display`, `std::error::Error`.
- `From` yazınca `?` kendiliğinden çevirir.
- `source` sebebi taşır, `Display` kendi cümlesini söyler.
- Kütüphanede enum, küçük uygulamada `Box<dyn Error>`.
- `main`'den dönen hata `Debug` ile yazılır; düzgün çıktı için `run` ve `ExitCode`.
