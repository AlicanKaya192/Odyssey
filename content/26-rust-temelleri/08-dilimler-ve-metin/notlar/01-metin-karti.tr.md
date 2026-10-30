## Oluşturmak

| Yazım | Sonuç |
|---|---|
| `String::new()` | Boş `String` |
| `String::from("a")` | `&str`'den `String` |
| `"a".to_string()` | Aynısı |
| `"a".to_owned()` | Aynısı |
| `format!("{a}-{b}")` | Birleştirip `String` |

Üçü de aynı işi yapar. Çoğu kod `String::from` ya da `.to_string()` yazar.

## Değiştirmek (`mut` gerekir)

| Metot | Ne yapar |
|---|---|
| `push('x')` | Tek karakter ekler |
| `push_str("xy")` | Metin ekler |
| `insert(0, 'x')` | Bayt konumuna ekler |
| `pop()` | Son karakteri çıkarır |
| `clear()` | Boşaltır |
| `truncate(n)` | `n` bayta kısaltır |

## Sorgulamak

| Metot | Döner |
|---|---|
| `len()` | Bayt sayısı |
| `chars().count()` | Harf sayısı |
| `is_empty()` | Boş mu |
| `contains("x")` | Var mı |
| `find("x")` | İlk bayt konumu, `Option` |
| `starts_with`, `ends_with` | Başlıyor, bitiyor mu |

## Bölmek

```rust
fn main() {
    let csv = "ada,36,london";
    for part in csv.split(',') {
        println!("{part}");
    }
    let (name, rest) = csv.split_once(',').unwrap();
    println!("{name} | {rest}");
    let text = "one\ntwo";
    for line in text.lines() {
        println!("{line}");
    }
}
```

```text
ada
36
london
ada | 36,london
one
two
```

## Karşılaştırmak

`String` ile `&str` doğrudan `==` ile karşılaştırılabilir. Büyük küçük harf duyarlıdır.

## Sayı ve metin

| Yön | Yazım |
|---|---|
| Sayıdan metne | `42.to_string()`, `format!("{n}")` |
| Metinden sayıya | `"42".parse::<i32>()` |

`parse` başarısız olabildiği için sonucu doğrudan sayı değildir. Sonraki bölümlerde `Result` olarak göreceğiz.
