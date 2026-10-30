# Trait'ler

Önceki bölümde `T: PartialOrd` yazdık. `PartialOrd` bir **trait**'ti: Bir türün neler yapabildiğini söyleyen sözleşme. Trait, başka dillerdeki "arayüz" (interface) fikrine yakındır: "Bu metotları sağlayan her tür benim için uygundur."

Bu bölümde kendi trait'imizi yazıyoruz.

## Trait tanımlamak

Trait yalnızca imzaları listeler. Gövdeyi her tür kendisi yazar:

```rust
trait Describe {
    fn describe(&self) -> String;
}

struct Book {
    title: String,
}

struct Coin {
    value: u32,
}

impl Describe for Book {
    fn describe(&self) -> String {
        format!("book: {}", self.title)
    }
}

impl Describe for Coin {
    fn describe(&self) -> String {
        format!("coin worth {}", self.value)
    }
}

fn main() {
    let book = Book { title: String::from("Dune") };
    let coin = Coin { value: 5 };
    println!("{}", book.describe());
    println!("{}", coin.describe());
}
```

```text
book: Dune
coin worth 5
```

| Parça | Anlamı |
|---|---|
| `trait Describe` | Sözleşmenin adı |
| `fn describe(&self) -> String;` | İstenen metot, noktalı virgülle biter |
| `impl Describe for Book` | "`Book` bu sözleşmeyi sağlıyor" |

Sözleşmedeki bir metot unutulursa derlenmez:

```rust
trait Greeter {
    fn hello(&self) -> String;
    fn bye(&self) -> String;
}

struct Robot;

impl Greeter for Robot {
    fn hello(&self) -> String {
        String::from("beep")
    }
}

fn main() {
    println!("{}", Robot.hello());
}
```

```text
error[E0046]: not all trait items implemented, missing: `bye`
 --> main.rs:8:1
  |
3 |     fn bye(&self) -> String;
  |     ------------------------ `bye` from trait
...
8 | impl Greeter for Robot {
  | ^^^^^^^^^^^^^^^^^^^^^^ missing `bye` in implementation
```

## Varsayılan gövde

Trait bir gövde de verebilir. Tür isterse üstüne yazar, istemezse hazır gelir:

```rust
trait Animal {
    fn name(&self) -> String;

    fn greet(&self) -> String {
        format!("Hello from {}", self.name())
    }
}

struct Dog;
struct Cat;

impl Animal for Dog {
    fn name(&self) -> String {
        String::from("Rex")
    }
}

impl Animal for Cat {
    fn name(&self) -> String {
        String::from("Tom")
    }

    fn greet(&self) -> String {
        String::from("...")
    }
}

fn main() {
    println!("{}", Dog.greet());
    println!("{}", Cat.greet());
}
```

```text
Hello from Rex
...
```

Varsayılan metot aynı trait'in öteki metotlarını çağırabilir. `Dog` yalnızca `name` yazdı, `greet` bedavaya geldi.

## Trait'i parametre olarak almak

Fonksiyon "bu trait'i sağlayan her tür" diyebilir. Kısa yazımı `impl Trait`:

```rust
trait Describe {
    fn describe(&self) -> String;
}

struct Book {
    title: String,
}

struct Coin {
    value: u32,
}

impl Describe for Book {
    fn describe(&self) -> String {
        format!("book: {}", self.title)
    }
}

impl Describe for Coin {
    fn describe(&self) -> String {
        format!("coin worth {}", self.value)
    }
}

fn show(item: &impl Describe) {
    println!("I see a {}", item.describe());
}

fn main() {
    show(&Book { title: String::from("Dune") });
    show(&Coin { value: 5 });
}
```

```text
I see a book: Dune
I see a coin worth 5
```

Aynı şeyin uzun yazımı generic kısıttır. İki yazım aynı işi yapar, seçim okunabilirliğe bağlıdır:

| Yazım | Fark |
|---|---|
| `fn f(x: &impl Describe)` | Kısa |
| `fn f<T: Describe>(x: &T)` | Aynı `T`'yi iki yerde isteyebilir |

Fark şurada görünür: `a` ve `b`'nin aynı tür olmasını istiyorsan generic yazmak zorundasın.

```rust
fn pair_max<T: PartialOrd + Copy>(a: T, b: T) -> T {
    if a > b { a } else { b }
}

fn main() {
    println!("{}", pair_max(1, 2));
    println!("{}", pair_max('x', 'a'));
}
```

```text
2
x
```

## Birden çok kısıt ve where

`+` kısıtları birleştirir. Kısıtlar uzayınca imza okunmaz olur, `where` onları aşağı alır:

```rust
use std::fmt::{Debug, Display};

fn report<T, U>(item: &T, extra: &U) -> String
where
    T: Display + Clone,
    U: Debug,
{
    format!("{} {:?}", item, extra)
}

fn main() {
    println!("{}", report(&5, &"note"));
}
```

```text
5 "note"
```

## impl Trait döndürmek

Fonksiyon "bu trait'i sağlayan bir şey döndürüyorum" diyebilir. Çağıran gerçek türü bilmez:

```rust
use std::fmt::Display;

fn make_label(n: i32) -> impl Display {
    format!("#{n}")
}

fn main() {
    let label = make_label(7);
    println!("{label}");
}
```

```text
#7
```

Tek bir şart var: Fonksiyon **tek bir** gerçek tür döndürmeli. İki farklı tür için bölüm 09'daki `dyn` gerekir:

```rust
use std::fmt::Display;

fn pick(flag: bool) -> impl Display {
    if flag {
        return 1;
    }
    "one"
}

fn main() {
    println!("{}", pick(true));
}
```

```text
error[E0308]: mismatched types
 --> main.rs:7:5
  |
3 | fn pick(flag: bool) -> impl Display {
  |                        ------------ expected a single type implementing `Display`
  because of return type
4 |     if flag {
5 |         return 1;
  |                - return type resolved to be `{integer}`
6 |     }
7 |     "one"
  |     ^^^^^ expected integer, found `&str`
  |
help: you could change the return type to be a boxed trait object
  |
3 - fn pick(flag: bool) -> impl Display {
3 + fn pick(flag: bool) -> Box<dyn Display> {
  |
help: if you change the return type to expect trait objects, box the returned
expressions
  |
5 ~         return Box::new(1);
6 |     }
7 ~     Box::new("one")
  |
```

## Kısıtlı impl

Bir `impl`, yalnızca kısıtı sağlayan türler için yazılabilir. Standart kütüphanede bu çok yaygındır: `Display` sağlayan her tür otomatik olarak `.to_string()` kazanır. Bunun adı **kapsayıcı impl** (blanket implementation):

```rust
use std::fmt::Display;

trait Shout {
    fn shout(&self) -> String;
}

impl<T: Display> Shout for T {
    fn shout(&self) -> String {
        self.to_string().to_uppercase()
    }
}

fn main() {
    println!("{}", "hi".shout());
    println!("{}", 42.shout());
}
```

```text
HI
42
```

`impl<T: Display> Shout for T`: "`Display` sağlayan her tür `Shout`'u da sağlar."

## Kimin trait'i, kimin türü?

Bir trait'i bir türe yazmak için **ikisinden biri senin olmalı.** `Vec`'e kendi trait'ini yazabilirsin, kendi türüne `Display` yazabilirsin. Başkasının trait'ini başkasının türüne yazamazsın:

```rust
use std::fmt::{self, Display};

impl Display for Vec<i32> {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "list")
    }
}

fn main() {
    println!("{}", vec![1]);
}
```

```text
error[E0117]: only traits defined in the current crate can be implemented for types
defined outside of the crate
 --> main.rs:3:1
  |
3 | impl Display for Vec<i32> {
  | ^^^^^^^^^^^^^^^^^--------
  |                  |
  |                  `Vec` is not defined in the current crate
  |
  = note: impl doesn't have any local type before any uncovered type parameters
  = note: for more information see
    https://doc.rust-lang.org/reference/items/implementations.html#orphan-rules
  = note: define and implement a trait or new type instead
```

Bu **yetim kuralı** (orphan rule), iki kütüphanenin aynı şeyi iki farklı biçimde yazıp çakışmasını önler.

## İlişkili türler

Trait, uygulayan türün seçeceği bir tür adı tanımlayabilir. `Iterator`'ın `Item`'ı böyledir (bölüm 05):

```rust
trait Measure {
    type Output;

    fn measure(&self) -> Self::Output;
}

struct Word(String);
struct Box2(f64, f64);

impl Measure for Word {
    type Output = usize;

    fn measure(&self) -> Self::Output {
        self.0.len()
    }
}

impl Measure for Box2 {
    type Output = f64;

    fn measure(&self) -> Self::Output {
        self.0 * self.1
    }
}

fn main() {
    println!("{}", Word(String::from("rust")).measure());
    println!("{}", Box2(1.5, 2.0).measure());
}
```

```text
4
3
```

`type Output = i32;` "Bu tür için `Output` budur." `Self::Output` onu kullanır. Generic parametreden farkı: Her tür için yalnızca **tek** seçim vardır.

## Özet

- `trait` sözleşmedir, `impl T for S` onu sağlar. Eksik metot derlenmez.
- Varsayılan gövde hazır gelir, üstüne yazılabilir.
- `&impl T` kısa yazım, `<X: T>` uzun yazım; aynı türü iki yerde istemek uzun yazım gerektirir.
- `+` birden çok kısıt, `where` uzun kısıtlar için.
- `-> impl T` tek gerçek tür döndürür.
- Yetim kuralı: Trait ya da tür senin olmalı.
- `type Output` ilişkili tür: Tür başına tek seçim.
