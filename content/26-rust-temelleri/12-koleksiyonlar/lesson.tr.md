# Vec ve HashMap

Dizinin boyutu sabitti. Gerçek programlarda kaç eleman geleceği çoğu zaman önceden bilinmez. **Koleksiyonlar** öbekte durur ve büyüyüp küçülebilir. En sık kullanılan iki tanesi `Vec` ve `HashMap`.

## Vec: Büyüyen liste

```rust
fn main() {
    let mut list: Vec<i32> = Vec::new();
    list.push(10);
    list.push(20);
    println!("{:?}", list);
    let ready = vec![1, 2, 3];
    println!("{}", ready.len());
    println!("{:?}", list.pop());
    println!("{:?}", list);
}
```

```text
[10, 20]
3
Some(20)
[10]
```

`Vec<i32>` "`i32` listesi" demektir. `vec![...]` makrosu hazır değerlerle oluşturur. `push` sona ekler, `pop` sondan çıkarır ve `Option` döndürür, çünkü liste boş olabilir.

## Elemana ulaşmak

İki yol var ve fark önemli:

```rust
fn main() {
    let v = vec![10, 20, 30];
    println!("{}", v[0]);
    println!("{:?}", v.get(0));
    println!("{:?}", v.get(9));
}
```

```text
10
Some(10)
None
```

| Yazım | Sınır dışında | Ne zaman |
|---|---|---|
| `v[9]` | **Panik** | Sınırda olduğundan eminsen |
| `v.get(9)` | `None` | Olmayabilirse |

## Gezmek

Önceki bölümde gördüğümüz üç biçim burada asıl anlamını buluyor:

```rust
fn main() {
    let mut v = vec![1, 2, 3];
    for n in &v {
        print!("{n} ");
    }
    println!();
    for n in &mut v {
        *n += 10;
    }
    println!("{:?}", v);
    for n in v {
        print!("{n} ");
    }
    println!();
}
```

```text
1 2 3
[11, 12, 13]
11 12 13
```

| Yazım | `n`'in türü | Sonra `v` |
|---|---|---|
| `for n in &v` | `&T` | Kullanılabilir |
| `for n in &mut v` | `&mut T` | Kullanılabilir, değişmiş |
| `for n in v` | `T` | **Taşındı** |

## Vec nasıl büyür?

`Vec`, `String` gibi üç parça tutar: adres, uzunluk, kapasite. Kapasite dolunca daha büyük bir yer alınıp bütün elemanlar oraya taşınır. Ölçelim:

```rust
fn main() {
    let mut v: Vec<i32> = Vec::new();
    let mut last = v.capacity();
    let mut moves = 0;
    for n in 0..1000 {
        v.push(n);
        if v.capacity() != last {
            last = v.capacity();
            moves += 1;
            print!("{last} ");
        }
    }
    println!();
    println!("{moves} moves");
}
```

```text
4 8 16 32 64 128 256 512 1024
9 moves
```

Kapasite ikiye katlanarak büyüyor, bu yüzden 1000 `push`'ta yalnızca birkaç kez taşınma oluyor. Boyutu önceden biliyorsan `Vec::with_capacity(n)` bu taşınmaları da önler.

Bu, önceki bölümde `E0502` veren örneğin gerçek sebebi: `push` belleği taşıyabilir.

## Sık kullanılan metotlar

```rust
fn main() {
    let mut v = vec![3, 1, 2, 3];
    println!("{}", v.contains(&2));
    v.sort();
    println!("{:?}", v);
    v.dedup();
    println!("{:?}", v);
    v.insert(0, 9);
    println!("{:?}", v);
    v.remove(1);
    println!("{:?}", v);
    v.retain(|n| *n != 2);
    println!("{:?}", v);
    println!("{:?} {:?}", v.first(), v.last());
}
```

```text
true
[1, 2, 3, 3]
[1, 2, 3]
[9, 1, 2, 3]
[9, 2, 3]
[9, 3]
Some(9) Some(3)
```

Dilimin bütün metotları `Vec`'te de çalışır (`len`, `contains`, `sort`, `iter`, `first`...), çünkü `&Vec<T>` kendiliğinden `&[T]`'ye dönüşür.

## HashMap: Anahtardan değere

`HashMap` değerleri bir **anahtarla** tutar: kullanıcı adından yaşa, kelimeden sayısına. Sıra numarası yerine anahtar kullanılır.

```rust
use std::collections::HashMap;

fn main() {
    let mut ages: HashMap<String, u32> = HashMap::new();
    ages.insert(String::from("Ada"), 36);
    ages.insert(String::from("Linus"), 55);
    ages.insert(String::from("Ada"), 37);
    println!("{:?}", ages.get("Ada"));
    println!("{:?}", ages.get("Grace"));
    println!("{}", ages.len());
    println!("{}", ages.contains_key("Linus"));
}
```

```text
Some(37)
None
2
true
```

`HashMap` otomatik gelmez, `use std::collections::HashMap;` gerekir. `insert` ekler (aynı anahtar varsa üstüne yazar), `get` `Option<&V>` döndürür.

## Sıra yok

`HashMap` elemanları **belirli bir sırada tutmaz.** Üstelik sıra her çalıştırmada değişebilir, çünkü Rust saldırılara karşı rastgele bir tohum kullanır. Sıra gerekiyorsa `BTreeMap` kullan ya da anahtarları sırala:

```rust
use std::collections::{BTreeMap, HashMap};

fn main() {
    let mut map = HashMap::new();
    map.insert("b", 2);
    map.insert("c", 3);
    map.insert("a", 1);
    let mut keys: Vec<_> = map.keys().collect();
    keys.sort();
    println!("{:?}", keys);

    let mut sorted = BTreeMap::new();
    sorted.insert("b", 2);
    sorted.insert("a", 1);
    println!("{:?}", sorted);
}
```

```text
["a", "b", "c"]
{"a": 1, "b": 2}
```

Bu bölümün alıştırmalarında `HashMap` çıktısı yazdırıyorsan önce sırala, yoksa çıktı rastgele olur.

## Sahiplik ve HashMap

`insert` anahtarın ve değerin sahipliğini alır:

```rust
use std::collections::HashMap;

fn main() {
    let key = String::from("Ada");
    let mut ages = HashMap::new();
    ages.insert(key, 36);
    println!("{key}");
}
```

```text
error[E0382]: borrow of moved value: `key`
 --> main.rs:7:16
  |
4 |     let key = String::from("Ada");
  |         --- move occurs because `key` has type `String`, which does not implement
  the `Copy` trait
5 |     let mut ages = HashMap::new();
6 |     ages.insert(key, 36);
  |                 --- value moved here
7 |     println!("{key}");
  |                ^^^ value borrowed here after move
  |
help: consider cloning the value if the performance cost is acceptable
  |
6 |     ages.insert(key.clone(), 36);
  |                    ++++++++
```

## entry: Yoksa ekle, varsa güncelle

En sık yapılan iş sayım. `entry` tam bunun içindir:

```rust
use std::collections::BTreeMap;

fn main() {
    let text = "the cat and the dog and the bird";
    let mut counts = BTreeMap::new();
    for word in text.split_whitespace() {
        let count = counts.entry(word).or_insert(0);
        *count += 1;
    }
    println!("{:?}", counts);
}
```

```text
{"and": 2, "bird": 1, "cat": 1, "dog": 1, "the": 3}
```

`.entry(word)` anahtarın yerini verir. `.or_insert(0)` yoksa 0 koyar ve değere `&mut` verir. `*count += 1` de onu artırır. Bu üç parça Rust'ın en çok gördüğün kalıbıdır.

Kelimeyi `&str` olarak anahtar yaptık: `text` yaşadıkça kopya gerekmez.

## Diğer koleksiyonlar

| Tür | Ne için |
|---|---|
| `Vec<T>` | Sıralı liste, varsayılan seçim |
| `VecDeque<T>` | İki uçtan hızlı ekleme ve çıkarma (kuyruk) |
| `HashMap<K, V>` | Anahtardan değere |
| `BTreeMap<K, V>` | Anahtara göre sıralı harita |
| `HashSet<T>` | Tekrarsız küme |
| `BTreeSet<T>` | Sıralı tekrarsız küme |

```rust
use std::collections::HashSet;

fn main() {
    let words = ["a", "b", "a", "c", "b"];
    let mut seen = HashSet::new();
    for word in words {
        if !seen.insert(word) {
            println!("again: {word}");
        }
    }
    println!("{}", seen.len());
}
```

```text
again: a
again: b
3
```

## Özet

- `Vec<T>` büyüyen listedir: `push`, `pop`, `v[i]` panikleyebilir, `v.get(i)` `Option` verir.
- `for x in &v` ödünç alır, `for x in v` tüketir.
- Kapasite ikiye katlanarak büyür; `push` belleği taşıyabilir.
- `HashMap` sıra tutmaz; yazdırmadan önce sırala ya da `BTreeMap` kullan.
- `insert` sahipliği alır. `entry(k).or_insert(v)` sayımın kalıbıdır.
