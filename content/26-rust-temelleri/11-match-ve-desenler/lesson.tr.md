# match ve Desenler

Önceki bölümde `match`'i gördük. Burada neden Rust'ın en güçlü araçlarından biri olduğunu göreceğiz: `match` yalnızca değer karşılaştırmaz, değerin **şeklini** tanır ve içini açar.

## match'in kuralları

```rust
enum Coin {
    One,
    Five,
    Ten,
}

fn value(coin: Coin) -> u32 {
    match coin {
        Coin::One => 1,
        Coin::Five => 5,
        Coin::Ten => 10,
    }
}

fn main() {
    println!("{}", value(Coin::Five));
}
```

```text
5
```

Her satıra **kol** (arm) denir: solda **desen** (pattern), `=>` sağında sonuç. Kollar yukarıdan aşağıya denenir, ilk tutan çalışır. `match` bir ifadedir, değer verir.

## Hiçbir durumu unutamazsın

`match` **kapsayıcı** (exhaustive) olmak zorundadır: Bütün durumlar ele alınmalıdır. Bir kolu silersek:

```rust
enum Coin {
    One,
    Five,
    Ten,
}

fn value(coin: Coin) -> u32 {
    match coin {
        Coin::One => 1,
        Coin::Five => 5,
    }
}

fn main() {
    println!("{}", value(Coin::Ten));
}
```

```text
error[E0004]: non-exhaustive patterns: `Coin::Ten` not covered
  --> main.rs:8:11
   |
 8 |     match coin {
   |           ^^^^ pattern `Coin::Ten` not covered
   |
note: `Coin` defined here
  --> main.rs:1:6
   |
 1 | enum Coin {
   |      ^^^^
...
 4 |     Ten,
   |     --- not covered
   = note: the matched value is of type `Coin`
help: ensure that all possible cases are being handled by adding a match arm with a
wildcard pattern or an explicit pattern as shown
   |
10 ~         Coin::Five => 5,
11 ~         Coin::Ten => todo!(),
   |
```

Derleyici eksik durumu adıyla söylüyor ve eklenecek satırı gösteriyor. Bunun değeri büyük projelerde ortaya çıkar: Enum'a yeni seçenek ekleyince derleyici onu ele almayan **bütün** yerleri listeler.

Kalan her şeyi tek kolda toplamak için `_` kullanılır. `_` değeri yakalamaz, "geri kalan" der:

```rust
fn describe(n: u8) -> &'static str {
    match n {
        0 => "zero",
        1 => "one",
        _ => "many",
    }
}

fn main() {
    println!("{} {} {}", describe(0), describe(1), describe(9));
}
```

```text
zero one many
```

`_` kullanmak kapsayıcılık denetimini kapatır: Yeni seçenek eklenince derleyici artık uyarmaz. Bu yüzden enum'larda mümkünse seçenekleri tek tek yaz.

## Değeri açmak

Desen, verinin içindeki parçaları değişkene bağlayabilir:

```rust
enum Message {
    Quit,
    Move { x: i32, y: i32 },
    Write(String),
}

fn handle(message: Message) -> String {
    match message {
        Message::Quit => String::from("bye"),
        Message::Move { x, y } => format!("move to {x} {y}"),
        Message::Write(text) => format!("write {text}"),
    }
}

fn main() {
    println!("{}", handle(Message::Move { x: 3, y: 4 }));
    println!("{}", handle(Message::Write(String::from("hi"))));
    println!("{}", handle(Message::Quit));
}
```

```text
move to 3 4
write hi
bye
```

- `Message::Move { x, y }` alanları aynı adlı değişkenlere açar.
- `Message::Write(text)` içindeki değeri `text`'e bağlar.
- `Message::Quit` veri taşımıyor.

Bu kol tek bir kalıpla hem seçeneği denetledi hem içini açtı. Başka dillerde bunun için önce tür denetlenir, sonra dönüştürülür ve bu iki adım birbirinden kopabilir.

## Desen çeşitleri

```rust
fn classify(n: i32) -> &'static str {
    match n {
        0 => "zero",
        1 | 2 => "small",
        3..=9 => "medium",
        n if n < 0 => "negative",
        _ => "large",
    }
}

fn main() {
    for n in [0, 2, 7, -4, 50] {
        println!("{n}: {}", classify(n));
    }
}
```

```text
0: zero
2: small
7: medium
-4: negative
50: large
```

| Desen | Anlamı |
|---|---|
| `0` | Tam bu değer |
| <code>1 &#124; 2</code> | Bu ya da şu |
| `3..=9` | Bu aralıkta |
| `n if n < 0` | **Koşul** (guard) ekler |
| `n` | Geri kalanı bağlar |

`|` burada "ya da"dır. `if` eklenen kola **koruma** (guard) denir: Desen tutsa bile koşul sağlanmazsa sonraki kola geçilir. Korumalı kollar kapsayıcılık sayılmaz, bu yüzden sonda yine `n` var.

Demet ve struct da açılır:

```rust
struct Point {
    x: i32,
    y: i32,
    z: i32,
}

fn main() {
    let pair = (3, 0);
    match pair {
        (0, 0) => println!("origin"),
        (x, 0) => println!("on x at {x}"),
        (_, y) => println!("y is {y}"),
    }
    let point = Point { x: 1, y: 2, z: 3 };
    let Point { x, .. } = point;
    println!("{x} {} {}", point.y, point.z);
}
```

```text
on x at 3
1 2 3
```

`..` kalan alanları atlar. `(x, 0)` "ikincisi 0 olan her demet"tir.

## Ödünç alarak eşleştirmek

Sahiplik burada da geçerli. `String` içeren bir değeri `match` ile açmak onu taşır:

```rust
fn main() {
    let value = Some(String::from("hi"));
    match value {
        Some(text) => println!("{text}"),
        None => println!("none"),
    }
    println!("{:?}", value);
}
```

```text
error[E0382]: borrow of partially moved value: `value`
 --> main.rs:7:22
  |
4 |         Some(text) => println!("{text}"),
  |              ---- value partially moved here
...
7 |     println!("{:?}", value);
  |                      ^^^^^ value borrowed here after partial move
  |
  = note: partial move occurs because value has type `String`, which does not implement
    the `Copy` trait
help: borrow this binding in the pattern to avoid moving the value
  |
4 |         Some(ref text) => println!("{text}"),
  |              +++
```

Çözüm değeri ödünç vermek: `match &value`. O zaman `text` bir `&String` olur:

```rust
fn main() {
    let value = Some(String::from("hi"));
    match &value {
        Some(text) => println!("{}", text.len()),
        None => println!("none"),
    }
    println!("{:?}", value);
}
```

```text
2
Some("hi")
```

Değiştirmek için `&mut`:

```rust
fn main() {
    let mut value = Some(String::from("hi"));
    if let Some(text) = &mut value {
        text.push_str(" there");
    }
    println!("{:?}", value);
}
```

```text
Some("hi there")
```

## if let ve let else

Yalnızca tek bir durum ilginçse `match` uzun kalır:

```rust
fn main() {
    let mut stack = vec![1, 2, 3];
    if let Some(top) = stack.last() {
        println!("top {top}");
    }
    while let Some(item) = stack.pop() {
        println!("popped {item}");
    }
}
```

```text
top 3
popped 3
popped 2
popped 1
```

`while let` döngü hâlidir: Desen tuttukça sürer. `let else` ise "desen tutmazsa hemen çık" der ve iç içeliği azaltır:

```rust
fn parse_pair(text: &str) -> String {
    let Some((key, value)) = text.split_once('=') else {
        return String::from("no equals sign");
    };
    format!("{key} is {value}")
}

fn main() {
    println!("{}", parse_pair("a=1"));
    println!("{}", parse_pair("oops"));
}
```

```text
a is 1
no equals sign
```

| Yazım | Ne zaman |
|---|---|
| `match` | Birkaç durum, hepsi önemli |
| `if let` | Tek durum önemli |
| `let else` | Tutmazsa erken çık, devamı düz yazılsın |
| `while let` | Desen tuttukça tekrar et |

## matches! makrosu

Yalnızca `bool` gerektiğinde:

```rust
fn main() {
    let grade = 'B';
    println!("{}", matches!(grade, 'A' | 'B'));
    println!("{}", matches!(Some(3), Some(n) if n > 5));
}
```

```text
true
false
```

## Özet

- `match` kapsayıcıdır: Durum unutmak `E0004` verir. Enum büyüyünce derleyici eksikleri gösterir.
- Desen değeri tanır ve açar: `Some(x)`, `Move { x, y }`, `(a, 0)`.
- `|`, `..=`, `if` koruması desenleri genişletir. `_` geri kalanı alır.
- `match &value` ödünç alarak açar, taşımaz.
- `if let`, `let else`, `while let` kısa yazımlardır; `matches!` `bool` verir.
