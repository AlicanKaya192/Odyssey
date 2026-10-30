# Fonksiyonlar ve İfadeler

Aynı işi tekrar tekrar yazmak yerine ona bir ad verip adıyla çağırırız. Bu ada sahip iş parçasına
**fonksiyon** denir. Şimdiye kadar yalnızca `main`'i yazdık; şimdi kendi fonksiyonlarımızı yazacağız.

## Fonksiyon tanımlamak

```rust
fn main() {
    say_hello();
    say_hello();
}

fn say_hello() {
    println!("Hello!");
}
```

```text
Hello!
Hello!
```

`fn` ile tanımlanır, adından sonra `()` ile **çağrılır**. Rust'ta tanım sırası önemli değildir:
`say_hello` burada `main`'in altında yazıldı ama yine çağrılabildi.

## Parametreler

Fonksiyona dışarıdan değer vermek için **parametre** yazarız. Rust'ta her parametrenin türü **zorunludur**,
derleyici çıkarmaz:

```rust
fn introduce(name: &str, age: i32) {
    println!("{name} is {age}");
}

fn main() {
    introduce("Ada", 36);
}
```

```text
Ada is 36
```

`name: &str` "name adında, metin türünde" demektir. `&str` metin türüdür; ne anlama geldiğini sahiplikten
sonra göreceğiz. Fonksiyonu çağırırken verdiğimiz `"Ada"` ve `36` değerlerine **argüman** denir.

Parametrelerde türün zorunlu olması tesadüf değil: Bir fonksiyonun imzası (adı, parametreleri, dönüş türü) onu
kullanan için bir sözleşmedir. Derleyici fonksiyonun içine bakmadan da çağrıyı denetleyebilir.

## Değer döndürmek

Fonksiyonun sonucunu geri vermesi için dönüş türünü `->` ile yazarız:

```rust
fn add(a: i32, b: i32) -> i32 {
    a + b
}

fn main() {
    let total = add(2, 3);
    println!("{total}");
}
```

```text
5
```

Dikkat: `a + b` satırının sonunda **noktalı virgül yok**. Bu Rust'ın en önemli alışkanlıklarından biri, çünkü
Rust'ta iki tür kod parçası vardır.

## Deyim ve ifade

- **İfade** (expression) bir değer üretir: `5`, `a + b`, `square(3)`.
- **Deyim** (statement) bir iş yapar, değer üretmez: `let x = 5;`.

Bir ifadenin sonuna noktalı virgül koyarsan onu deyime çevirirsin ve değeri atılır. Fonksiyonun son satırındaki
ifade noktalı virgülsüzse onun değeri dönüş değeri olur. Noktalı virgül koyarsan hata alırsın:

```rust
fn square(n: i32) -> i32 {
    n * n;
}

fn main() {
    println!("{}", square(3));
}
```

```text
error[E0308]: mismatched types
 --> main.rs:1:22
  |
1 | fn square(n: i32) -> i32 {
  |    ------            ^^^ expected `i32`, found `()`
  |    |
  |    implicitly returns `()` as its body has no tail or `return` expression
2 |     n * n;
  |          - help: remove this semicolon to return this value
```

Derleyici tam olarak bunu söylüyor: Fonksiyon `i32` vaat etti ama gövdesi hiçbir şey vermedi ve `help:` satırı
noktalı virgülü silmeni öneriyor. Bu hatayı çok göreceksin. Görünce ilk bakacağın yer son satırın sonu.

## Bloklar da ifadedir

Süslü parantezli her blok bir ifadedir ve son satırının değerini verir:

```rust
fn main() {
    let area = {
        let width = 4;
        let height = 5;
        width * height
    };
    println!("{area}");
}
```

```text
20
```

`if` de ifadedir; bunu sonraki bölümde kullanacağız.

## return ile erken dönmek

Son satırdan önce çıkmak için `return` yazılır:

```rust
fn safe_half(n: i32) -> i32 {
    if n < 0 {
        return 0;
    }
    n / 2
}

fn main() {
    println!("{}", safe_half(10));
    println!("{}", safe_half(-4));
}
```

```text
5
0
```

`if` bir koşul sınar; `n` sıfırdan küçükse süslü parantezin içi çalışır. Ayrıntısı sonraki bölümde. `return` kullanılabilir ama Rust'ta alışkanlık şudur: Sonda yalnızca değeri yaz, `return`'ü **erken çıkış** için sakla.

## Değer döndürmeyen fonksiyon

`->` yazılmazsa fonksiyon birim (`()`) döndürür, yani anlamlı bir değer vermez. `main` de böyledir. Birimi
yazdırmak istersen `{:?}` gerekir:

```rust
fn greet() {
    println!("hi");
}

fn main() {
    let nothing = greet();
    println!("{:?}", nothing);
}
```

```text
hi
()
```

## Birden fazla değer döndürmek

Demet bu iş için çok uygundur:

```rust
fn min_max(a: i32, b: i32) -> (i32, i32) {
    (a.min(b), a.max(b))
}

fn main() {
    let (low, high) = min_max(9, 4);
    println!("{low} {high}");
}
```

```text
4 9
```

`let (low, high) = ...` satırı dönen demeti iki değişkene açıyor.

## Yorum satırları

Kod içine not bırakmak için `//` kullanılır. Üç eğik çizgi `///` belge yorumudur: Hemen altındaki öğeyi anlatır
ve `cargo doc` onlardan belge sayfası üretir.

```rust
/// Returns the area of a rectangle.
fn area(width: u32, height: u32) -> u32 {
    // Width and height are never negative, so u32 is enough.
    width * height
}

fn main() {
    println!("{}", area(3, 4));
}
```

```text
12
```

Yorum "ne yaptığını" değil, kod kendini anlatamadığında "neden öyle yaptığını" yazmalıdır.

## Özet

- `fn ad(parametre: tür) -> dönüş_türü { ... }`. Parametre türleri zorunludur.
- Son satırdaki noktalı virgülsüz ifade dönüş değeridir. Noktalı virgül koymak `E0308` hatası verir.
- İfade değer üretir, deyim üretmez. Bloklar da ifadedir.
- `return` erken çıkış içindir.
- Birden fazla değer demetle döndürülür.
