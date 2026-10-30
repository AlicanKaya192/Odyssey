# Iterator'lar

Listeyi `for` ile gezip bir şey toplamak Rust'ta en sık yazılan koddur. **Iterator** bu işi parçalara ayırır: Süz, dönüştür, topla. Kod kısalır, niyeti okunur ve hız kaybı olmaz.

## Iterator nedir?

"Sıradaki elemanı ver" diyebildiğin her şey. Trait'in özü tek metottur:

```text
trait Iterator {
    type Item;
    fn next(&mut self) -> Option<Self::Item>;
}
```

`next` eleman varken `Some(eleman)`, bitince `None` döndürür:

```rust
fn main() {
    let list = vec![10, 20];
    let mut it = list.iter();
    println!("{:?}", it.next());
    println!("{:?}", it.next());
    println!("{:?}", it.next());
}
```

```text
Some(10)
Some(20)
None
```

`next` iterator'ın yerini değiştirdiği için `let mut` gerekiyor.

## Üç gezme yolu

Sahiplik burada da karar verir:

```rust
fn main() {
    let mut v = vec![1, 2];
    for x in v.iter() {
        print!("{x} ");
    }
    for x in v.iter_mut() {
        *x *= 10;
    }
    println!("{:?}", v);
    for x in v.into_iter() {
        print!("{x} ");
    }
    println!();
}
```

```text
1 2 [10, 20]
10 20
```

| Metot | Eleman türü | Liste sonra |
|---|---|---|
| `.iter()` | `&T` | Duruyor |
| `.iter_mut()` | `&mut T` | Duruyor, değişmiş olabilir |
| `.into_iter()` | `T` | Tüketildi |

`for x in &v`, `for x in &mut v` ve `for x in v` yazımları bunların kısa hâlidir.

## Tembellik

`map` ve `filter` tek başına **hiçbir şey yapmaz.** Yalnızca "ne yapılacağını" kurar. İş, birisi eleman isteyince başlar:

```rust
fn main() {
    let list = vec![1, 2];
    let _ignored = list.iter().map(|x| println!("first map {x}"));
    println!("nothing ran yet");
    let out: Vec<i32> = list
        .iter()
        .map(|x| {
            println!("second map {x}");
            x * 2
        })
        .collect();
    println!("{:?}", out);
}
```

```text
nothing ran yet
second map 1
second map 2
[2, 4]
```

İlk `map` hiç çalışmadı: Çıktıda yalnızca `collect`'ten sonra satır var. Derleyici de uyarır: "iterator adapters are lazy". İki tür metot var:

| Tür | Örnek | Ne döndürür |
|---|---|---|
| **Uyarlayıcı** (adapter) | `map`, `filter`, `take`, `rev` | Yeni iterator, tembel |
| **Tüketici** (consumer) | `collect`, `sum`, `count`, `max`, `for` | Sonuç, işi başlatır |

Bir eleman bütün zinciri tek seferde geçer. Bütün liste önce `map`'ten sonra `filter`'dan geçmez:

```rust
fn main() {
    let out: Vec<i32> = [1, 2, 3, 4]
        .iter()
        .map(|x| {
            println!("map {x}");
            x * 2
        })
        .filter(|x| {
            println!("filter {x}");
            *x > 2
        })
        .take(1)
        .collect();
    println!("{:?}", out);
}
```

```text
map 1
filter 2
map 2
filter 4
[4]
```

`take(1)` yetince geri kalanlara hiç bakılmadı. Bu yüzden iterator zinciri gereksiz iş yapmaz.

## En sık uyarlayıcılar

```rust
fn main() {
    let v = vec![1, 2, 3, 4];
    let doubled: Vec<i32> = v.iter().map(|x| x * 2).collect();
    let big: Vec<&i32> = v.iter().filter(|x| **x > 2).collect();
    let some: Vec<&i32> = v.iter().skip(1).take(2).collect();
    println!("{:?} {:?} {:?}", doubled, big, some);
    for (i, x) in v.iter().enumerate().rev().take(1) {
        println!("{i} {x}");
    }
    let pairs: Vec<(i32, char)> = vec![1, 2].into_iter().zip("ab".chars()).collect();
    println!("{:?}", pairs);
    let flat: Vec<char> = ["ab", "c"].iter().flat_map(|s| s.chars()).collect();
    println!("{:?}", flat);
}
```

```text
[2, 4, 6, 8] [3, 4] [2, 3]
3 4
[(1, 'a'), (2, 'b')]
['a', 'b', 'c']
```

| Metot | İş |
|---|---|
| `map(f)` | Dönüştür |
| `filter(f)` | Koşula uyanı tut (`&Item` alır) |
| `take(n)`, `skip(n)` | İlk `n`, ilk `n`'i atla |
| `enumerate()` | `(sıra, eleman)` |
| `zip(diğer)` | İkisini yan yana |
| `rev()` | Ters çevir |
| `chain(diğer)` | Arka arkaya |
| `flat_map(f)` | Listeleri düzleştir |

`filter` neden `**n` istiyor? `.iter()` `&i32` verir, `filter` ona bir referans daha ekler: `&&i32`. Çoğu zaman desenle açarsın: `|&&n| n > 1`.

## En sık tüketiciler

```rust
fn main() {
    let v = vec![3, 8, 5];
    println!("{}", v.iter().sum::<i32>());
    println!("{}", v.iter().count());
    println!("{:?} {:?}", v.iter().max(), v.iter().min());
    println!("{:?}", v.iter().find(|x| **x > 4));
    println!("{:?}", v.iter().position(|x| *x == 5));
    println!("{} {}", v.iter().any(|x| *x > 7), v.iter().all(|x| *x > 7));
}
```

```text
16
3
Some(8) Some(3)
Some(8)
Some(2)
true false
```

`find` ilk eşleşmeyi, `position` onun sırasını, `any` ve `all` `bool` verir. `max` ve `min` `Option` döndürür, çünkü liste boş olabilir.

## collect

`collect` istediğin koleksiyona toplar; hedef türü sen söylersin:

```rust
use std::collections::{HashMap, HashSet};

fn main() {
    let list: Vec<i32> = (1..4).collect();
    let text: String = "abc".chars().rev().collect();
    let unique: HashSet<i32> = [1, 1, 2].into_iter().collect();
    let map: HashMap<&str, i32> = [("a", 1)].into_iter().collect();
    println!("{:?} {text} {} {:?}", list, unique.len(), map.get("a"));
    let good: Result<Vec<i32>, _> = ["1", "2"].iter().map(|s| s.parse::<i32>()).collect();
    let bad: Result<Vec<i32>, _> = ["1", "x"].iter().map(|s| s.parse::<i32>()).collect();
    println!("{:?} {}", good, bad.is_err());
}
```

```text
[1, 2, 3] cba 2 Some(1)
Ok([1, 2]) true
```

`Result<Vec<_>, _>` özellikle güçlüdür: Biri bile hatalıysa ilk hata döner.

## fold

Bütün tüketicilerin annesi. Başlangıç değeri ve "yeni değeri nasıl birleştiririm" sorusu:

```rust
fn main() {
    let v = [1, 2, 3];
    let total = v.iter().fold(0, |sum, x| sum + x);
    let text = v.iter().fold(String::new(), |acc, x| format!("{acc}{x}-"));
    println!("{total} {text}");
}
```

```text
6 1-2-3-
```

`sum` aslında `fold(0, |a, b| a + b)` gibidir. Hazır metot varsa onu kullan; `fold` özel birikim içindir.

## Döngü mü, iterator mü?

```rust
fn with_loop(v: &[i32]) -> i32 {
    let mut total = 0;
    for x in v {
        if x % 2 == 0 {
            total += x * x;
        }
    }
    total
}

fn with_iter(v: &[i32]) -> i32 {
    v.iter().filter(|x| **x % 2 == 0).map(|x| x * x).sum()
}

fn main() {
    let v = [1, 2, 3, 4];
    println!("{} {}", with_loop(&v), with_iter(&v));
}
```

```text
20 20
```

İkisi aynı sonucu verir ve derlenince hızları aynıdır. Rust'ın sıfır maliyetli soyutlama (zero-cost abstraction) sözü bu: Yüksek düzeyli yazım, elle yazılmış döngü kadar hızlı çalışır. Dizi sınırı denetimi de çoğu zaman kalkar.

Dönüştürme ve toplama için iterator daha okunur. Karmaşık erken çıkış ve birden çok değişken güncelleme için `for` daha açıktır. Zorlama.

## Özet

- `next` `Some` ya da `None` verir. `iter`, `iter_mut`, `into_iter` sahipliği seçer.
- Uyarlayıcılar tembeldir, tüketici işi başlatır. Eleman zinciri tek tek geçer.
- `map`, `filter`, `take`, `enumerate`, `zip`, `rev`, `chain`, `flat_map`.
- `collect`, `sum`, `count`, `max`, `find`, `any`, `all`, `fold`.
- `collect` hedef türü ister, `Result<Vec<_>, _>` ilk hatada durur.
- Iterator elle yazılmış döngü kadar hızlıdır.
