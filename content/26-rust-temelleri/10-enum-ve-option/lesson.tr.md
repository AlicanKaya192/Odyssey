# Enum ve Option

Struct "şu **ve** şu" der: bir kullanıcının adı **ve** yaşı var. Bazı şeyler ise "şu **ya da** şu"dur: bir ödeme ya nakit ya da karttır. **Enum** bu ikinci duruma karşılık gelir.

## Enum tanımlamak

```rust
enum Light {
    Red,
    Yellow,
    Green,
}

fn advice(light: Light) -> &'static str {
    match light {
        Light::Red => "stop",
        Light::Yellow => "wait",
        Light::Green => "go",
    }
}

fn main() {
    println!("{}", advice(Light::Green));
    println!("{}", advice(Light::Red));
}
```

```text
go
stop
```

`enum` olası **seçenekleri** (variant) listeler. Bir değişken aynı anda yalnızca birini tutar. Seçeneklere `Tur::Secenek` ile ulaşılır.

Karşılaştırmak için `match` kullanılır. `match` bütün seçenekleri ele almak zorundadır; ayrıntısını sonraki bölümde göreceğiz.

## Seçenekler veri taşıyabilir

Rust enum'larını sıradan listelerden ayıran şey budur: Her seçenek kendi verisini taşır.

```rust
#[derive(Debug)]
enum Payment {
    Cash,
    Card(String),
    Transfer { iban: String, amount: u32 },
}

fn main() {
    let payments = [
        Payment::Cash,
        Payment::Card(String::from("1234")),
        Payment::Transfer { iban: String::from("TR00"), amount: 50 },
    ];
    for p in &payments {
        println!("{:?}", p);
    }
}
```

```text
Cash
Card("1234")
Transfer { iban: "TR00", amount: 50 }
```

`Cash` veri taşımıyor, `Card` bir metin, `Transfer` iki alan taşıyor. Bunların hepsi tek bir türün değerleridir, yani aynı listede ya da aynı fonksiyon parametresinde durabilirler.

Struct ile yazmaya kalksak her seçenek için alan açıp çoğunu boş bırakmamız ve "kart seçiliyse iban boş olmalı" gibi kuralları kendimiz korumamız gerekirdi. Enum ile **geçersiz durum yazılamaz** hâle gelir.

<figure class="fig"><div class="versus"><div><h4>Struct ile</h4><code>kind: String, card: String, iban: String</code><br>Bütün alanlar her zaman var. Kart seçiliyken <code>iban</code> ne olacak?</div><div><h4>Enum ile</h4><code>Cash | Card(String) | Transfer { .. }</code><br>Her seçenek yalnızca kendi verisini taşır.</div></div><figcaption>Rust programcılarının sevdiği cümle: Geçersiz durumu yazılamaz yap.</figcaption></figure>

Enum'lara da `impl` ile metot yazılır:

```rust
#[derive(Debug)]
enum Payment {
    Cash,
    Card(String),
    Transfer { iban: String, amount: u32 },
}

impl Payment {
    fn describe(&self) -> String {
        match self {
            Payment::Cash => String::from("cash"),
            Payment::Card(number) => format!("card {number}"),
            Payment::Transfer { amount, .. } => format!("transfer of {amount}"),
        }
    }
}

fn main() {
    println!("{}", Payment::Card(String::from("1234")).describe());
    let paid = Payment::Transfer { iban: String::from("TR00"), amount: 50 };
    println!("{}", paid.describe());
}
```

```text
card 1234
transfer of 50
```

## null yok, Option var

Çoğu dilde "değer yok" anlamında `null` vardır ve her değişken `null` olabilir. Bu, programların en sık çökme sebeplerinden biridir: `null`'un mucidi onu "milyar dolarlık hatam" diye anmıştır.

Rust'ta `null` yoktur. "Değer olmayabilir" türün içinde açıkça yazılır. Bunun için standart kütüphanede bir enum hazırdır:

```rust
enum Option<T> {
    Some(T),
    None,
}
```

`T` "herhangi bir tür" demektir (generic'ler ikinci modülde). `Option<i32>` ya bir sayı taşır ya hiçbir şey. `Some` ve `None` her yerde kullanılabilir, `use` gerekmez:

```rust
fn main() {
    let some_number: Option<i32> = Some(5);
    let no_number: Option<i32> = None;
    println!("{:?}", some_number);
    println!("{:?}", no_number);
    println!("{}", some_number.is_some());
}
```

```text
Some(5)
None
true
```

## Option ile sayı toplanamaz

`Option<i32>` ile `i32` farklı türlerdir. Değer olmayabileceği için derleyici seni önce ona bakmaya zorlar:

```rust
fn main() {
    let a: i32 = 5;
    let b: Option<i32> = Some(3);
    println!("{}", a + b);
}
```

```text
error[E0277]: cannot add `Option<i32>` to `i32`
 --> main.rs:4:22
  |
4 |     println!("{}", a + b);
  |                      ^ no implementation for `i32 + Option<i32>`
  |
  = help: the trait `Add<Option<i32>>` is not implemented for `i32`
help: the following other types implement trait `Add<Rhs>`
 --> /rustc/58cf8f9c35b355199727627d07ae34a4e2846d67/library\core\src\ops\arith.rs:98:8
  |
  = note: `i32` implements `Add`
 ::: /rustc/58cf8f9c35b355199727627d07ae34a4e2846d67/library\core\src\ops\arith.rs:113:0
  |
  = note: in this macro invocation
 -->
 /rustc/58cf8f9c35b355199727627d07ae34a4e2846d67/library\core\src\internal_macros.rs:22:8
  |
  = note: `&i32` implements `Add<i32>`
 :::
 /rustc/58cf8f9c35b355199727627d07ae34a4e2846d67/library\core\src\internal_macros.rs:33:8
  |
  = note: `i32` implements `Add<&i32>`
 :::
 /rustc/58cf8f9c35b355199727627d07ae34a4e2846d67/library\core\src\internal_macros.rs:44:8
  |
  = note: `&i32` implements `Add`
  = note: this error originates in the macro `add_impl` (in Nightly builds, run with -Z
    macro-backtrace for more info)
```

Bu hata sinir bozucu görünür ama `null` sorununun tam çözümüdür: **Bir değerin yokluğunu unutmak derlenmez.** Türü `i32` olan bir değişkenin kesinlikle sayı olduğundan emin olursun.

## Option'dan değer almak

`match` en açık yoldur:

```rust
fn describe(value: Option<i32>) -> String {
    match value {
        Some(n) => format!("got {n}"),
        None => String::from("nothing"),
    }
}

fn main() {
    println!("{}", describe(Some(3)));
    println!("{}", describe(None));
}
```

```text
got 3
nothing
```

Tek bir durum ilginçse `if let` daha kısadır:

```rust
fn main() {
    let value = Some(7);
    if let Some(n) = value {
        println!("{n}");
    }
    let empty: Option<i32> = None;
    if let Some(n) = empty {
        println!("{n}");
    } else {
        println!("empty");
    }
}
```

```text
7
empty
```

Hazır metotlar çok işi tek satırda çözer:

```rust
fn main() {
    let full = Some(5);
    let empty: Option<i32> = None;
    println!("{}", full.unwrap_or(0));
    println!("{}", empty.unwrap_or(0));
    println!("{:?}", full.map(|x| x * 2));
    println!("{:?}", empty.map(|x| x * 2));
}
```

```text
5
0
Some(10)
None
```

| Metot | `Some(5)` | `None` |
|---|---|---|
| `unwrap()` | 5 | **Panik** |
| `expect("mesaj")` | 5 | **Mesajla panik** |
| `unwrap_or(0)` | 5 | 0 |
| `is_some()` | `true` | `false` |
| <code>map(&#124;x&#124; x * 2)</code> | `Some(10)` | `None` |

`|x| x * 2` kısa bir fonksiyondur (**closure**), ikinci modülde ayrıntılı göreceğiz: "x alır, x * 2 döndürür".

## unwrap'ten kaçın

`unwrap` değer yoksa programı durdurur:

```rust
fn main() {
    let empty: Option<i32> = None;
    println!("{}", empty.unwrap());
}
```

```text
thread 'main' panicked at main.rs:3:26:
called `Option::unwrap()` on a `None` value
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

Kısa örneklerde ve "burada kesinlikle değer var" dediğin yerlerde kullanılabilir, ama gerçek programda `match`, `if let` ya da `unwrap_or` daha iyidir. Bir düşün: Değer yoksa programın gerçekten ölmesi mi gerekiyor?

## Standart kütüphane Option döndürür

Olmayabilecek her şey `Option` verir. Bunu baştan beri kullanıyorduk:

```rust
fn main() {
    let days = [10, 20, 30];
    println!("{:?}", days.get(1));
    println!("{:?}", days.get(9));
    println!("{:?}", "hello".find('l'));
    println!("{:?}", "hello".find('z'));
    println!("{:?}", days.first());
}
```

```text
Some(20)
None
Some(2)
None
Some(10)
```

`.get(1)` elemanı `Some` içinde verir, `.get(9)` paniklemek yerine `None` verir. Yani `v[9]` panikler, `v.get(9)` panikmez.

## Özet

- Enum "ya şu ya bu"dur; seçenekler kendi verisini taşıyabilir.
- `Option<T>`, `Some(değer)` ya da `None`'dur. Rust'ta `null` yoktur.
- `Option<i32>` ile `i32` karışmaz: yokluğu unutmak derlenmez.
- Değer almak için `match`, `if let`, `unwrap_or`. `unwrap` değer yoksa panikler.
- Olmayabilecek değerler döndüren fonksiyonlar `Option` döndürür.
