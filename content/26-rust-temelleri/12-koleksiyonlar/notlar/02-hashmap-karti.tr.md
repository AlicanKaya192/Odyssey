## HashMap metotları

| Metot | Ne yapar | Döner |
|---|---|---|
| `insert(k, v)` | Ekler ya da üstüne yazar | Eski değer, `Option` |
| `get(&k)` | Bakar | `Option<&V>` |
| `get_mut(&k)` | Değiştirmek için bakar | `Option<&mut V>` |
| `remove(&k)` | Siler | `Option<V>` |
| `contains_key(&k)` | Var mı | `bool` |
| `len()`, `is_empty()` | Boyut | |
| `keys()`, `values()` | Gezer | iterator |
| `entry(k)` | Yerini verir | `Entry` |

## entry kalıpları

```rust
use std::collections::BTreeMap;

fn main() {
    let pairs = [("fruit", "apple"), ("veg", "leek"), ("fruit", "pear")];
    let mut groups: BTreeMap<&str, Vec<&str>> = BTreeMap::new();
    for (kind, name) in pairs {
        groups.entry(kind).or_default().push(name);
    }
    println!("{:?}", groups);

    let mut totals: BTreeMap<&str, i32> = BTreeMap::new();
    *totals.entry("a").or_insert(10) += 1;
    *totals.entry("a").or_insert(10) += 1;
    println!("{:?}", totals);
}
```

```text
{"fruit": ["apple", "pear"], "veg": ["leek"]}
{"a": 12}
```

| Yazım | Ne zaman |
|---|---|
| `.or_insert(0)` | Yoksa bu değer |
| `.or_default()` | Yoksa türün varsayılanı |
| `.or_insert_with(Vec::new)` | Yoksa hesapla |

Bir anahtara birden çok değer biriktirmek için `HashMap<K, Vec<V>>` ve `.or_default().push(x)`.

## Hangi türler anahtar olur?

Anahtar türü `Eq` ve `Hash` özelliklerini sağlamalıdır. Tam sayılar, `char`, `bool`, `String`, `&str` olur. **`f64` olmaz**, çünkü `NaN` kendisine eşit değildir. Kendi struct'ın için `#[derive(PartialEq, Eq, Hash)]`.

## HashMap mi, BTreeMap mi?

| Soru | Seçim |
|---|---|
| Sıra önemli değil, hız önemli | `HashMap` |
| Sıralı gezmek ya da aralık sorgusu gerekiyor | `BTreeMap` |
| Çıktı her çalıştırmada aynı olmalı | `BTreeMap` ya da sırala |
