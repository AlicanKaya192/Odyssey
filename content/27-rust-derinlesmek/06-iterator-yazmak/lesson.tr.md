# Kendi Iterator'ın

Önceki bölümde hazır iterator kullandık. Şimdi kendi türümüze `Iterator` yazıyoruz. Karşılığı büyük: **Tek bir `next` yazınca** `map`, `filter`, `sum`, `take` ve onlarca metot bedavaya gelir.

## En küçük örnek

```rust
struct Counter {
    count: u32,
}

impl Iterator for Counter {
    type Item = u32;

    fn next(&mut self) -> Option<u32> {
        if self.count >= 3 {
            return None;
        }
        self.count += 1;
        Some(self.count)
    }
}

fn main() {
    let mut c = Counter { count: 0 };
    println!("{:?}", c.next());
    println!("{:?}", c.next());
    println!("{:?}", c.next());
    println!("{:?}", c.next());
}
```

```text
Some(1)
Some(2)
Some(3)
None
```

Parçalar:

| Parça | Anlamı |
|---|---|
| `type Item = u32;` | Hangi tür elemanlar çıkacak (ilişkili tür) |
| `fn next(&mut self)` | Sıradakini ver, durumu ilerlet |
| `None` | Bitti |

Durum struct'ın içinde tutulur: İterator "nerede kaldığını" kendisi hatırlar.

## Bedava metotlar

Yalnızca `next` yazdık, ama:

```rust
struct Counter {
    count: u32,
}

impl Iterator for Counter {
    type Item = u32;

    fn next(&mut self) -> Option<u32> {
        if self.count >= 3 {
            return None;
        }
        self.count += 1;
        Some(self.count)
    }
}

fn main() {
    let total: u32 = Counter { count: 0 }.sum();
    let list: Vec<u32> = Counter { count: 0 }.map(|x| x * 10).collect();
    let odd = Counter { count: 0 }.filter(|x| x % 2 == 1).count();
    println!("{total} {:?} {odd}", list);
    for n in (Counter { count: 1 }) {
        print!("{n} ");
    }
    println!();
}
```

```text
6 [10, 20, 30] 2
2 3
```

`Iterator` trait'inin varsayılan metotları `next`'i çağırır. `for` da aynı yolu kullanır.

## Sonsuz iterator

`next` hiç `None` döndürmeyebilir. Tembellik sayesinde sorun değildir, `take` ile keseriz:

```rust
struct Fibonacci {
    a: u64,
    b: u64,
}

impl Iterator for Fibonacci {
    type Item = u64;

    fn next(&mut self) -> Option<u64> {
        let out = self.a;
        self.a = self.b;
        self.b += out;
        Some(out)
    }
}

fn main() {
    let first: Vec<u64> = Fibonacci { a: 0, b: 1 }.take(8).collect();
    println!("{:?}", first);
    let big = Fibonacci { a: 0, b: 1 }.find(|n| *n > 100);
    println!("{:?}", big);
}
```

```text
[0, 1, 1, 2, 3, 5, 8, 13]
Some(144)
```

`collect` ya da `sum`'ı `take` olmadan çağırırsan program sonsuza kadar çalışır, çünkü tüketici sonu bekler.

## Ödünç veren iterator

Bir koleksiyonun elemanlarına referans veren iterator, koleksiyondan uzun yaşayamaz. Yaşam süresi işareti burada gerçekten gerekir:

```rust
struct Pairs<'a, T> {
    items: &'a [T],
    position: usize,
}

impl<'a, T> Iterator for Pairs<'a, T> {
    type Item = (&'a T, &'a T);

    fn next(&mut self) -> Option<Self::Item> {
        if self.position + 1 >= self.items.len() {
            return None;
        }
        let pair = (&self.items[self.position], &self.items[self.position + 1]);
        self.position += 1;
        Some(pair)
    }
}

fn main() {
    let list = [1, 2, 3];
    let mut it = Pairs { items: &list, position: 0 };
    let a = it.next();
    let b = it.next();
    println!("{:?} {:?} {:?}", a, b, it.next());
}
```

```text
Some((1, 2)) Some((2, 3)) None
```

`type Item = &'a T`: Dönen referans `self`'e değil **dilime** bağlı. Bu yüzden `next` iki kez çağrılıp iki referans aynı anda tutulabilir.

## into_iter: for ile çalışması için

`for x in nesne` yazabilmek için `IntoIterator` gerekir. Standart kalıp, koleksiyon için üç biçim sunmaktır. En sık olanı `&Koleksiyon`:

```rust
struct Shelf {
    books: Vec<String>,
}

impl<'a> IntoIterator for &'a Shelf {
    type Item = &'a String;
    type IntoIter = std::slice::Iter<'a, String>;

    fn into_iter(self) -> Self::IntoIter {
        self.books.iter()
    }
}

fn main() {
    let shelf = Shelf { books: vec![String::from("Dune"), String::from("Emma")] };
    for book in &shelf {
        println!("{book}");
    }
    println!("{}", shelf.books.len());
}
```

```text
Dune
Emma
2
```

`impl<'a> IntoIterator for &'a Shelf`: "`&Shelf` iterator'a dönüşebilir." Böylece `for book in &shelf` çalışır ve `shelf` sonra da kullanılabilir.

## Hazır araçlarla üretmek

Her iterator için struct yazman gerekmez:

```rust
use std::iter;

fn main() {
    let a: Vec<i32> = iter::repeat(7).take(2).collect();
    let mut n = 0;
    let b: Vec<i32> = iter::from_fn(|| {
        n += 1;
        if n < 4 { Some(n) } else { None }
    })
    .collect();
    let step = |x: &u32| if *x < 50 { Some(x * 3) } else { None };
    let c: Vec<u32> = iter::successors(Some(1), step).collect();
    let d: Vec<i32> = (0..10).step_by(4).collect();
    println!("{:?} {:?} {:?} {:?}", a, b, c, d);
}
```

```text
[7, 7] [1, 2, 3] [1, 3, 9, 27, 81] [0, 4, 8]
```

| Araç | Ne üretir |
|---|---|
| `std::iter::repeat(x)` | Sonsuz `x` |
| `std::iter::once(x)` | Tek eleman |
| `std::iter::from_fn(f)` | `f` `None` diyene kadar |
| `std::iter::successors(a, f)` | Her eleman öncekinden |
| `(0..n)`, `(0..).step_by(k)` | Aralıklar |

## iterator döndürmek

Zinciri fonksiyondan döndürmek için tür adını yazmana gerek yok:

```rust
fn evens(list: &[i32]) -> impl Iterator<Item = i32> + '_ {
    list.iter().copied().filter(|x| x % 2 == 0)
}

fn main() {
    let list = [1, 2, 3, 4];
    let total: i32 = evens(&list).map(|x| x * 10).sum();
    println!("{total}");
}
```

```text
60
```

`impl Iterator<Item = i32> + '_`: `'_` "girdiye bağlı" demektir, çünkü dönen iterator dilimi ödünç tutuyor.

## Özet

- `impl Iterator for S`, `type Item`, `fn next(&mut self) -> Option<Item>`.
- Tek `next` bütün uyarlayıcı ve tüketicileri kazandırır.
- Sonsuz iterator tembellik sayesinde güvenlidir; `take` ile kes.
- Ödünç veren iterator `struct S<'a>` ve `type Item = &'a T` ister.
- `IntoIterator for &'a S` `for x in &s` yazımını açar.
- `from_fn`, `successors`, `repeat` struct yazmadan iterator üretir.
- `-> impl Iterator<Item = T>` zinciri döndürür.
