# Generic'ler

Aynı işi yapan iki fonksiyon düşün: Biri `i32` listesinin en büyüğünü buluyor, öteki `char` listesinin. Gövdeleri harfi harfine aynı, yalnızca türler farklı. **Generic**, türü bir değişken gibi yazmaktır: Kodu bir kez yazarsın, her türle çalışır.

Bunu aslında çoktan kullanıyorsun. `Vec<i32>`, `Option<String>`, `Result<i32, String>` hep generic türler.

## Tekrarın sorunu

```rust
fn largest_number(list: &[i32]) -> &i32 {
    let mut top = &list[0];
    for item in list {
        if item > top {
            top = item;
        }
    }
    top
}

fn largest_letter(list: &[char]) -> &char {
    let mut top = &list[0];
    for item in list {
        if item > top {
            top = item;
        }
    }
    top
}

fn main() {
    println!("{}", largest_number(&[3, 9, 2]));
    println!("{}", largest_letter(&['a', 'z', 'm']));
}
```

```text
9
z
```

İki fonksiyon, tek fikir. Bir hata bulursan iki yerde düzeltirsin.

## Generic fonksiyon

Tür parametresi köşeli parantezde, fonksiyon adından hemen sonra yazılır. Gelenek olarak kısa bir büyük harftir: `T` (type).

```rust
fn largest<T>(list: &[T]) -> &T {
```

"`largest`, herhangi bir `T` türü için çalışır" diye okunur. Ama bu kadarı derlenmez:

```rust
fn largest<T>(list: &[T]) -> &T {
    let mut top = &list[0];
    for item in list {
        if item > top {
            top = item;
        }
    }
    top
}

fn main() {
    println!("{}", largest(&[3, 9, 2]));
}
```

```text
error[E0369]: binary operation `>` cannot be applied to type `&T`
 --> main.rs:4:17
  |
4 |         if item > top {
  |            ---- ^ --- &T
  |            |
  |            &T
  |
help: consider restricting type parameter `T` with trait `PartialOrd`
  |
1 | fn largest<T: std::cmp::PartialOrd>(list: &[T]) -> &T {
  |             ++++++++++++++++++++++
```

Derleyici haklı: `T` herhangi bir tür olabilir, her tür `>` ile karşılaştırılamaz. Öneriyi de kendisi veriyor: `T`'nin karşılaştırılabilir olduğunu söyle.

```rust
fn largest<T: PartialOrd>(list: &[T]) -> &T {
    let mut top = &list[0];
    for item in list {
        if item > top {
            top = item;
        }
    }
    top
}

fn main() {
    println!("{}", largest(&[3, 9, 2]));
    println!("{}", largest(&['a', 'z', 'm']));
    println!("{}", largest(&[1.5, 0.5]));
    let words = [String::from("pear"), String::from("apple")];
    println!("{}", largest(&words));
}
```

```text
9
z
1.5
pear
```

`T: PartialOrd` bir **kısıttır** (bound): "`T` yalnızca karşılaştırılabilen bir tür olabilir." `PartialOrd` bir **trait**: Bir türün neler yapabildiğini söyleyen bir sözleşme. Traitleri bir sonraki bölümde yazacağız. Şimdilik bilmen gereken: Generic kod `T` hakkında yalnızca kısıtta söylenenleri kullanabilir.

Fonksiyon `&T` döndürüyor, kopya istemiyor. Bu yüzden `String` listesiyle de çalışıyor, `String` kopyalanamadığı hâlde.

## Generic struct

```rust
#[derive(Debug)]
struct Point<T> {
    x: T,
    y: T,
}

fn main() {
    let a = Point { x: 1, y: 2 };
    let b = Point { x: 1.5, y: 2.5 };
    println!("{:?} {:?}", a, b);
}
```

```text
Point { x: 1, y: 2 } Point { x: 1.5, y: 2.5 }
```

`x` ve `y` aynı `T`. Farklı olsalar derlenmez:

```rust
#[derive(Debug)]
struct Point<T> {
    x: T,
    y: T,
}

fn main() {
    let a = Point { x: 1, y: 2.5 };
    println!("{:?}", a);
}
```

```text
error[E0308]: mismatched types
 --> main.rs:8:30
  |
8 |     let a = Point { x: 1, y: 2.5 };
  |                              ^^^ expected integer, found floating-point number
```

İki tür istiyorsan iki parametre yaz:

```rust
#[derive(Debug)]
struct Pair<A, B> {
    first: A,
    second: B,
}

fn main() {
    let pair = Pair { first: 1, second: "one" };
    println!("{:?}", pair);
    println!("{}", pair.second);
}
```

```text
Pair { first: 1, second: "one" }
one
```

## Generic metotlar

`impl`'in de tür parametresini tanıtması gerekir, yoksa `T`'yi gerçek bir tür adı sanır:

```rust
#[derive(Debug)]
struct Point<T> {
    x: T,
    y: T,
}

impl<T> Point<T> {
    fn new(x: T, y: T) -> Point<T> {
        Point { x, y }
    }

    fn x(&self) -> &T {
        &self.x
    }
}

impl Point<f64> {
    fn length(&self) -> f64 {
        (self.x * self.x + self.y * self.y).sqrt()
    }
}

fn main() {
    let a = Point::new(3, 4);
    println!("{}", a.x());
    let b = Point::new(3.0, 4.0);
    println!("{}", b.length());
}
```

```text
3
5
```

`impl<T> Point<T>` "her `T` için", `impl Point<f64>` "yalnızca `f64` için" demektir. İkinci bloktaki metot `Point<i32>` üzerinde yoktur:

```rust
struct Point<T> {
    x: T,
    y: T,
}

impl Point<f64> {
    fn length(&self) -> f64 {
        (self.x * self.x + self.y * self.y).sqrt()
    }
}

fn main() {
    let a = Point { x: 3, y: 4 };
    println!("{}", a.length());
}
```

```text
error[E0599]: no method named `length` found for struct `Point<{integer}>` in the
current scope
  --> main.rs:14:22
   |
 1 | struct Point<T> {
   | --------------- method `length` not found for this struct
...
14 |     println!("{}", a.length());
   |                      ^^^^^^ method not found in `Point<{integer}>`
   |
   = note: the method was found for `Point<f64>`
```

Kısıt da yalnızca gereken metoda konur. Bir `Point<T>` her tür için oluşturulabilir, ama `larger` için `T`'nin karşılaştırılabilir olması gerekir:

```rust
#[derive(Debug)]
struct Point<T> {
    x: T,
    y: T,
}

impl<T: PartialOrd + Copy> Point<T> {
    fn larger(&self) -> T {
        if self.x > self.y {
            self.x
        } else {
            self.y
        }
    }
}

fn main() {
    println!("{}", Point { x: 3, y: 9 }.larger());
    println!("{}", Point { x: 'b', y: 'a' }.larger());
}
```

```text
9
b
```

## Generic enum

`Option` ve `Result` artık sır değil. Standart kütüphanede kabaca şöyle yazılıdır:

```text
enum Option<T> {
    Some(T),
    None,
}

enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

Kendi generic enum'unu da yazabilirsin:

```rust
#[derive(Debug)]
enum Reply<T> {
    Found(T),
    Missing,
}

fn find(list: &[i32], wanted: i32) -> Reply<usize> {
    for (index, item) in list.iter().enumerate() {
        if *item == wanted {
            return Reply::Found(index);
        }
    }
    Reply::Missing
}

fn main() {
    println!("{:?}", find(&[5, 7], 7));
    println!("{:?}", find(&[5, 7], 9));
    let text: Reply<&str> = Reply::Found("hi");
    println!("{:?}", text);
}
```

```text
Found(1)
Missing
Found("hi")
```

## Tür belirtmek: turbofish

Derleyici çoğu zaman `T`'yi çıkarır. Çıkaramazsa açıkça söylersin. `::<...>` yazımının lakabı **turbofish**'tir:

```rust
fn main() {
    let n = "42".parse::<i32>().unwrap();
    let empty = Vec::<i32>::new();
    let letters = "abc".chars().collect::<Vec<_>>();
    println!("{n} {} {:?}", empty.len(), letters);
}
```

```text
42 0 ['a', 'b', 'c']
```

`_` "bu kısmı sen bul" demektir: `Vec<_>`.

## Bedeli var mı?

Yok. Derleyici generic kodu kullandığın her tür için ayrı ayrı üretir. Buna **monomorfizasyon** (monomorphization) denir:

<figure class="fig"><div class="flow"><span class="node">largest&lt;T&gt;</span><span class="arrow">→</span><span class="node ok">largest için i32</span><span class="arrow">→</span><span class="node ok">largest için char</span></div><figcaption>Derleme bitince generic kalmaz; elle yazılmış gibi ayrı fonksiyonlar vardır.</figcaption></figure>

Çalışma anında yavaşlık olmaz. Karşılığı: Her tür için yeni kod üretildiğinden derleme biraz uzar ve program biraz büyür.

Tür boyutunu da ölçelim:

```rust
use std::mem::size_of;

struct Point<T> {
    x: T,
    y: T,
}

fn main() {
    println!("{}", size_of::<i32>());
    println!("{}", size_of::<Point<i32>>());
    println!("{}", size_of::<Point<f64>>());
    println!("{}", size_of::<Point<u8>>());
}
```

```text
4
8
16
2
```

`Point<f64>` tam olarak iki `f64`'tür: Fazladan hiçbir şey taşımaz.

## Sabit generic'ler

Tür değil, sayı da parametre olabilir. Dizinin boyutu türünün parçası olduğu için işe yarar:

```rust
fn total<const N: usize>(values: [i32; N]) -> i32 {
    let mut sum = 0;
    for v in values {
        sum += v;
    }
    sum
}

fn main() {
    println!("{}", total([1, 2, 3]));
    println!("{}", total([1, 2, 3, 4, 5]));
}
```

```text
6
15
```

`const N: usize` "derleme zamanında bilinen bir sayı" demektir. `[i32; 3]` ve `[i32; 5]` için ayrı kopyalar üretilir.

## Özet

- `fn f<T>(...)`, `struct S<T>`, `enum E<T>`, `impl<T> S<T>`: Tür parametresi köşeli parantezde.
- Generic kod `T` hakkında yalnızca kısıtta yazılanı kullanır: `T: PartialOrd`.
- `impl<T> S<T>` her tür için, `impl S<f64>` yalnızca o tür için.
- `::<T>` (turbofish) türü açıkça verir; `_` geri kalanını derleyiciye bırakır.
- Monomorfizasyon: Her tür için ayrı kod üretilir, çalışma anında bedeli yok.
- `const N: usize` sayıyı da parametre yapar.
