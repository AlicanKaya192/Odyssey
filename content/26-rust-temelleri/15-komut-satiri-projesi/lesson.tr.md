# Bitirme: Komut Satırı Aracı

Şimdiye kadar öğrendiklerini tek bir gerçek programda birleştiriyoruz: Dosyada kelime arayan küçük bir araç. Adı `search`, Linux'taki `grep`'in çok küçük bir akrabası.

```text
search rust notes.txt --ignore-case
```

Satırları numarasıyla yazacak. Çıkış kodları da `grep` gibi:

| Kod | Anlamı |
|---|---|
| `0` | Bulundu |
| `1` | Bulunamadı |
| `2` | Hata (eksik argüman, okunamayan dosya) |

**Çıkış kodu** programın bitince işletim sistemine bıraktığı sayıdır. `0` "sorun yok" demektir ve başka programlar buna bakarak karar verir.

Yeni olan her şey küçük: Argüman okumak, dosya okumak, stderr'e yazmak ve test yazmak.

## Argümanlar

Program adından sonra yazılanlar `std::env::args` ile okunur:

```rust
use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();
    println!("{} values", args.len());
    println!("{}", args[1]);
    println!("{}", args[2]);
}
```

```text
3 values
rust
notes.txt
```

`env::args()` bir iterator verir, `collect` onu `Vec<String>`'e toplar. **İlk eleman programın kendi yoludur**, asıl argümanlar `args[1]`'den başlar. Yukarıdaki kod bu yüzden `args.len()` ile sayıyor ve ilk elemanı yazdırmıyor: Yol makineye göre değişir.

## Dosya okumak

`std::fs::read_to_string` bütün dosyayı `String` olarak verir. Dosya olmayabilir, bu yüzden `Result` döndürür:

```rust
use std::fs;

fn main() {
    match fs::read_to_string("notes.txt") {
        Ok(text) => {
            for line in text.lines() {
                println!("{line}");
            }
        }
        Err(_) => println!("cannot read the file"),
    }
    if fs::read_to_string("missing.txt").is_err() {
        println!("missing.txt: cannot read the file");
    }
}
```

```text
Rust is fast
Python is easy
rust has no garbage collector
missing.txt: cannot read the file
```

`text.lines()` metni satırlara böler. Satır sonu işareti satıra dahil değildir, Windows'taki `\r\n` de buna dahildir.

Hatanın kendi mesajını yazdırmadık, çünkü işletim sisteminin diline göre değişir. Program yalnızca kendi cümlesini yazıyor. Gerçek bir araçta kendi cümlenin yanına `{e}` ile sistemin mesajını da ekleyebilirsin.

## Ayarlar: Config

Dağınık değişkenler yerine bir struct. Argümanları ayrıştırmak da `main`'den ayrı bir fonksiyon, çünkü ayrı fonksiyon test edilebilir:

```rust
struct Config {
    pattern: String,
    path: String,
    ignore_case: bool,
}

fn parse_args(args: &[String]) -> Result<Config, String> {
    if args.len() < 3 {
        return Err(String::from("usage: search <pattern> <file> [--ignore-case]"));
    }
    Ok(Config {
        pattern: args[1].clone(),
        path: args[2].clone(),
        ignore_case: args.len() > 3 && args[3] == "--ignore-case",
    })
}

```

`&[String]` bir dilim: Fonksiyon listeyi ödünç alıyor. `.clone()` metnin kopyasını alır, çünkü `Config` kendi metnine sahip olmalı.

## Arama

Asıl iş ekrana hiçbir şey yazmıyor. Girdi alıyor, sonuç döndürüyor:

```rust
fn search(pattern: &str, text: &str, ignore_case: bool) -> Vec<String> {
    let wanted = if ignore_case { pattern.to_lowercase() } else { pattern.to_string() };
    let mut found = Vec::new();
    for (index, line) in text.lines().enumerate() {
        let candidate = if ignore_case { line.to_lowercase() } else { line.to_string() };
        if candidate.contains(&wanted) {
            found.push(format!("{}: {}", index + 1, line));
        }
    }
    found
}

```

Metni küçük harfe çevirmek, karşılaştırmanın büyük harfi görmezden gelmesini sağlıyor. Bulunan satırın kendisi ise özgün hâliyle yazılıyor.

## Çalıştırma

`run` parçaları birleştirir. Hata türü `String`, `?` onu yukarı iletir:

```rust
fn run(config: &Config) -> Result<usize, String> {
    let text = fs::read_to_string(&config.path)
        .map_err(|_| format!("cannot read {}", config.path))?;
    let found = search(&config.pattern, &text, config.ignore_case);
    for line in &found {
        println!("{line}");
    }
    Ok(found.len())
}

```

## main: stdout, stderr ve çıkış kodu

```rust
fn main() {
    let args: Vec<String> = env::args().collect();
    let config = match parse_args(&args) {
        Ok(config) => config,
        Err(message) => {
            eprintln!("{message}");
            process::exit(2);
        }
    };
    match run(&config) {
        Ok(0) => process::exit(1),
        Ok(_) => {}
        Err(message) => {
            eprintln!("error: {message}");
            process::exit(2);
        }
    }
}

```

Burada iki yeni şey var:

| Yazım | Ne yapar |
|---|---|
| `eprintln!` | `println!` gibi, ama **stderr**'e yazar |
| `process::exit(n)` | Programı `n` koduyla hemen bitirir |

Sonuçlar stdout'a, hatalar stderr'e gider. Böylece `search rust notes.txt > out.txt` yazıldığında dosyaya yalnızca sonuçlar girer.

Deneyelim:

{{F_session}}

## Düzen hakkında

Kodda `main` çok kısa, asıl iş `search`'te. Bu düzen rastlantı değil:

<figure class="fig"><div class="flow"><span class="node">main</span><span class="arrow">→</span><span class="node">parse_args</span><span class="arrow">→</span><span class="node">run</span><span class="arrow">→</span><span class="node ok">search</span></div><figcaption>Girdi ve çıktı uçlarda, yan etkisiz iş ortada. Test edilmesi en kolay yer de orası.</figcaption></figure>

Proje büyürse `search` ve `parse_args` `src/lib.rs`'e taşınır, `main.rs`'te yalnızca `main` kalır.

## İlk testler

Rust'ta test yazmak için ek bir paket gerekmez. Test, üstünde `#[test]` yazan bir fonksiyondur:

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn finds_the_line() {
        let found = search("rust", "a\nrust b", false);
        assert_eq!(found, vec!["2: rust b"]);
    }

    #[test]
    fn ignores_case_when_asked() {
        assert_eq!(search("RUST", "rust", false).len(), 0);
        assert_eq!(search("RUST", "rust", true).len(), 1);
    }
}

```

`cargo test` testleri çalıştırır (burada yalnızca test bölümünü gösteriyoruz):

{{F_tests}}

| Parça | Anlamı |
|---|---|
| `#[cfg(test)]` | Bu modül yalnızca test derlemesinde var |
| `use super::*;` | Üst modüldeki her şeyi al |
| `#[test]` | Bu bir test |
| `assert_eq!(a, b)` | Eşit değilse test düşer |

Test düşünce ne olur? Bilerek bozalım:

{{F_testfail}}

`left` ve `right` iki tarafın gerçek değerlerini gösterir.

**İyi test gerçekten hata yakalayan testtir.** Kodu bilerek boz, test düşmüyorsa yeterli değildir. Bu bölümün son alıştırması bunu ölçüyor.

## Özet

- `env::args().collect()` argümanları verir; ilk eleman programın yoludur.
- `fs::read_to_string` dosyayı okur ve `Result` döndürür; `.lines()` satırlara böler.
- Sonuç stdout'a (`println!`), hata stderr'e (`eprintln!`), durum çıkış koduna (`process::exit`).
- Yan etkisiz işi ayrı fonksiyona koy, test edilebilir olsun.
- `#[cfg(test)]`, `#[test]`, `assert_eq!` ve `cargo test` test yazmanın dört parçasıdır.

Bu modülün son bölümünde her şeyi tekrar edeceğiz.
