# Genel Tekrar

Bu modülde hiç programlama bilmeden başladın ve Rust'ın en zor fikirlerine kadar geldin. Bu bölüm yeni bir şey öğretmiyor, parçaları birleştiriyor. Sınav bütün modülden karışık, alıştırmalar birkaç konuyu birlikte istiyor.

## Tek programda modül

Aşağıdaki program modülün çoğunu kullanıyor. Her satırı açıklayabiliyorsan bu modül tamamdır:

```rust
use std::collections::BTreeMap;

#[derive(Debug, PartialEq, Eq, PartialOrd, Ord, Clone, Copy)]
enum Kind {
    Income,
    Expense,
}

struct Item {
    kind: Kind,
    amount: i32,
}

fn parse(line: &str) -> Result<Item, String> {
    let (word, number) = line.split_once(' ').ok_or("no space")?;
    let amount = number.parse::<i32>().map_err(|_| format!("bad amount: {number}"))?;
    let kind = match word {
        "in" => Kind::Income,
        "out" => Kind::Expense,
        other => return Err(format!("bad kind: {other}")),
    };
    Ok(Item { kind, amount })
}

fn main() {
    let mut items = Vec::new();
    for line in ["in 100", "out 30", "out x", "gift 5", "out 20"] {
        match parse(line) {
            Ok(item) => items.push(item),
            Err(message) => println!("skipped: {message}"),
        }
    }
    let mut totals = BTreeMap::new();
    for item in &items {
        *totals.entry(item.kind).or_insert(0) += item.amount;
    }
    println!("{:?}", totals);
}
```

```text
skipped: bad amount: x
skipped: bad kind: gift
{Income: 100, Expense: 50}
```

| Satır | Konu |
|---|---|
| `enum Kind` ve `#[derive]` | Enum ve özellik türetme |
| `struct Item` | Struct |
| `fn parse(line: &str)` | Dilim ve ödünç alma |
| `-> Result<Item, String>` | Hata yönetimi |
| `split_once`, `?`, `map_err` | Metin ve hata iletimi |
| `match` | Desen eşleştirme, her dal zorunlu |
| `BTreeMap`, `entry` | Koleksiyonlar |
| `for item in &items` | Ödünç alarak gezmek |

## En önemli üç fikir

**1. Sahiplik.** Her değerin tek sahibi var. Sahip kapsamdan çıkınca değer silinir. Atama `Copy` olmayan türü taşır.

```rust
fn main() {
    let a = String::from("hi");
    let b = a;
    println!("{a} {b}");
}
```

```text
error[E0382]: borrow of moved value: `a`
 --> main.rs:4:16
  |
2 |     let a = String::from("hi");
  |         - move occurs because `a` has type `String`, which does not implement the
  `Copy` trait
3 |     let b = a;
  |             - value moved here
4 |     println!("{a} {b}");
  |                ^ value borrowed here after move
  |
help: consider cloning the value if the performance cost is acceptable
  |
3 |     let b = a.clone();
  |              ++++++++
```

**2. Ödünç alma.** Aynı anda ya birçok okuyucu ya da tek yazıcı. Referans sahibinden uzun yaşayamaz.

```rust
fn main() {
    let mut list = vec![1];
    let first = &list[0];
    list.push(2);
    println!("{first}");
}
```

```text
error[E0502]: cannot borrow `list` as mutable because it is also borrowed as immutable
 --> main.rs:4:5
  |
3 |     let first = &list[0];
  |                  ---- immutable borrow occurs here
4 |     list.push(2);
  |     ^^^^^^^^^^^^ mutable borrow occurs here
5 |     println!("{first}");
  |                ----- immutable borrow later used here
```

**3. Eksikliği türe yaz.** `null` ve istisna yok. Olmayabilirse `Option`, başarısız olabilirse `Result`. Derleyici unutmana izin vermez.

```rust
fn first_word(text: &str) -> Option<&str> {
    text.split_whitespace().next()
}

fn main() {
    match first_word("  hello world") {
        Some(word) => println!("{word}"),
        None => println!("empty"),
    }
    println!("{:?}", first_word("   "));
}
```

```text
hello
None
```

## Derleyici hatası okumak

Rust'ta en sık yapacağın iş bu. Sırayla bak:

| Adım | Nerede |
|---|---|
| 1. Kod | `error[E0382]` |
| 2. Yer | `--> main.rs:4:20` |
| 3. Etiketler | `^^^ value borrowed here after move` |
| 4. Öneri | `help: consider cloning` |

Her öneri doğru değildir: `clone` çoğu zaman derlemeyi sağlar ama asıl çözüm ödünç almaktır. Önce "bu değerin sahibi kim olmalı?" diye sor.

## Hangisini seçmeli?

| Soru | Seçim |
|---|---|
| Fonksiyon değeri yalnızca okuyacak | `&T`, metinde `&str`, listede `&[T]` |
| Fonksiyon yerinde değiştirecek | `&mut T` |
| Fonksiyon sahiplenecek | `T` |
| Değer olmayabilir | `Option<T>` |
| İşlem başarısız olabilir | `Result<T, E>` |
| Büyüyen liste | `Vec<T>` |
| Anahtardan değere | `HashMap`, sıralıysa `BTreeMap` |
| Birkaç seçenekten biri | `enum` |
| Birlikte duran alanlar | `struct` |

## Özet

Bir sonraki modülde özellikler (traits), generic türler, ömürler ve closure'lar var. Bunlar bu modüldeki sahiplik fikrinin üstüne kuruluyor; sahiplik oturmadıysa önce 06 ve 07'ye dön.
