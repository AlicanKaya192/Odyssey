# Genel Tekrar

Bu modül Rust'ı "derleyiciyle kavga etmeden yazmak"tan "soyutlamayı bedelsiz kurmak"a taşıdı. Bu bölüm yeni bir şey öğretmiyor, parçaları birleştiriyor. Sınav bütün modülden karışık, alıştırmalar birkaç konuyu aynı anda istiyor.

## Tek programda modül

Aşağıdaki program modülün çoğunu kullanıyor. Her satırı açıklayabiliyorsan bu modül tamamdır:

```rust
use std::error::Error;
use std::fmt;
use std::num::ParseIntError;
use std::sync::Mutex;
use std::thread;

#[derive(Debug)]
enum OrderError {
    NoColon(String),
    BadQuantity(ParseIntError),
}

impl fmt::Display for OrderError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            OrderError::NoColon(line) => write!(f, "no colon in {line}"),
            OrderError::BadQuantity(_) => write!(f, "bad quantity"),
        }
    }
}

impl Error for OrderError {}

impl From<ParseIntError> for OrderError {
    fn from(e: ParseIntError) -> Self {
        OrderError::BadQuantity(e)
    }
}

struct Order<'a> {
    name: &'a str,
    quantity: u32,
}

fn parse<'a>(line: &'a str) -> Result<Order<'a>, OrderError> {
    let (name, quantity) = line
        .split_once(':')
        .ok_or_else(|| OrderError::NoColon(line.to_string()))?;
    Ok(Order { name, quantity: quantity.trim().parse()? })
}

fn parse_all<'a>(lines: &[&'a str]) -> Result<Vec<Order<'a>>, OrderError> {
    lines.iter().map(|line| parse(line)).collect()
}

trait Pricing: Sync {
    fn price(&self, order: &Order) -> u32;
}

struct Flat(u32);
struct Bulk;

impl Pricing for Flat {
    fn price(&self, order: &Order) -> u32 {
        self.0 * order.quantity
    }
}

impl Pricing for Bulk {
    fn price(&self, order: &Order) -> u32 {
        if order.quantity >= 10 { order.quantity * 2 } else { order.quantity * 3 }
    }
}

fn main() -> Result<(), Box<dyn Error>> {
    let orders = parse_all(&["pen: 3", "ink: 12"])?;
    let rules: Vec<Box<dyn Pricing>> = vec![Box::new(Flat(5)), Box::new(Bulk)];

    for rule in &rules {
        let total = Mutex::new(0);
        thread::scope(|s| {
            for order in &orders {
                let (total, rule) = (&total, rule);
                s.spawn(move || *total.lock().unwrap() += rule.price(order));
            }
        });
        println!("{}", total.lock().unwrap());
    }

    let names: Vec<&str> = orders.iter().map(|order| order.name).collect();
    println!("{names:?}");

    if let Err(e) = parse_all(&["pen"]) {
        println!("{e}");
    }
    Ok(())
}
```

```text
75
33
["pen", "ink"]
no colon in pen
```

| Yer | Konu |
|---|---|
| `enum OrderError`, `impl Error`, `From` | Hata tasarımı |
| `struct Order<'a>` | Ömür: Metin satırdan ödünç |
| `trait Pricing`, `Box<dyn Pricing>` | Trait ve trait nesnesi |
| `fn parse_all<'a>` ve `collect` | Iterator, Result toplamak |
| `thread::scope`, `Mutex` | Aynı anda çalışmak, kilit |
| `|order| ...` | Kapanış |

## En önemli dört fikir

**1. Trait, davranışı sözleşmeye yazar.** Generic kod yalnızca sınırında yazanı kullanabilir:

```rust
fn largest<T>(list: &[T]) -> &T {
    let mut best = &list[0];
    for item in list {
        if item > best {
            best = item;
        }
    }
    best
}

fn main() {
    println!("{}", largest(&[1, 2]));
}
```

```text
error[E0369]: binary operation `>` cannot be applied to type `&T`
 --> main.rs:4:17
  |
4 |         if item > best {
  |            ---- ^ ---- &T
  |            |
  |            &T
  |
help: consider restricting type parameter `T` with trait `PartialOrd`
  |
1 | fn largest<T: std::cmp::PartialOrd>(list: &[T]) -> &T {
  |             ++++++++++++++++++++++
```

**2. Ömür, ödünç almanın kanıtıdır.** Değeri uzatmaz; derleyiciye girdiyle çıktının bağını söyler:

```rust
fn longer(a: &str, b: &str) -> &str {
    if a.len() > b.len() { a } else { b }
}

fn main() {
    println!("{}", longer("a", "bb"));
}
```

```text
error[E0106]: missing lifetime specifier
 --> main.rs:1:32
  |
1 | fn longer(a: &str, b: &str) -> &str {
  |              ----     ----     ^ expected named lifetime parameter
  |
  = help: this function's return type contains a borrowed value, but the signature does
    not say whether it is borrowed from `a` or `b`
help: consider introducing a named lifetime parameter
  |
1 | fn longer<'a>(a: &'a str, b: &'a str) -> &'a str {
  |          ++++     ++          ++          ++
```

**3. Kollar arasında güvenliği türler sağlar.** `Rc` kola geçmez, çünkü `Send` değildir. Veri yarışı çalışma anında bulunmaz, derlenmez:

```rust
use std::rc::Rc;
use std::thread;

fn main() {
    let shared = Rc::new(1);
    let handle = thread::spawn(move || println!("{shared}"));
    handle.join().unwrap();
}
```

```text
error[E0277]: `Rc<i32>` cannot be sent between threads safely
 --> main.rs:6:32
  |
6 |     let handle = thread::spawn(move || println!("{shared}"));
  |                  ------------- -------^^^^^^^^^^^^^^^^^^^^^
  |                  |             |
  |                  |             `Rc<i32>` cannot be sent between threads safely
  |                  |             within this `{closure@main.rs:6:32: 6:39}`
  |                  required by a bound introduced by this call
  |
  = help: within `{closure@main.rs:6:32: 6:39}`, the trait `Send` is not implemented for
    `Rc<i32>`
note: required because it's used within this closure
 --> main.rs:6:32
  |
6 |     let handle = thread::spawn(move || println!("{shared}"));
  |                                ^^^^^^^
note: required by a bound in `spawn`
```

**4. Hata bir değerdir ve tasarlanır.** Çağıran duruma göre karar verebilsin diye enum, `?` çevirsin diye `From`.

## Hangi araç?

| İhtiyaç | Araç |
|---|---|
| Aynı kod, farklı türler, hız | Generic |
| Aynı listede farklı türler | `Box<dyn Trait>` |
| Boyutu bilinmeyen tür, özyineleme | `Box<T>` |
| Çok sahip, tek kol | `Rc<T>` |
| Paylaşılan değeri değiştirmek, tek kol | `Rc<RefCell<T>>` |
| Çok sahip, çok kol | `Arc<T>` |
| Değiştirmek, çok kol | `Arc<Mutex<T>>` |
| Veri göndermek, kollar arası | `mpsc::channel` |

## Tekrar sorusu

Kendine sor: Şunları bakmadan yazabiliyor musun?

- `impl Iterator for X` ve üstüne `map`, `filter`, `sum`.
- `Fn`, `FnMut`, `FnOnce` farkı ve `move`.
- Bir `enum` hata türü: `Display`, `Error`, `From`.
- `thread::scope` içinde parçalara bölünmüş iş.
- `#[should_panic]` ve bozuk kodu yakalayan test.

Takıldığın olursa o bölümün ders notuna dön. Alıştırmalar bu listeyi deniyor.

## Özet

- Trait + generic: Bedelsiz soyutlama. Trait nesnesi: Çalışma anında seçim.
- Ömür yalnızca ilişkiyi yazar, değeri uzatmaz.
- Akıllı işaretçi seçimi: Kaç sahip, kaç kol, değişiyor mu?
- Hata türü tasarımdır; test ve Clippy alışkanlıktır.
