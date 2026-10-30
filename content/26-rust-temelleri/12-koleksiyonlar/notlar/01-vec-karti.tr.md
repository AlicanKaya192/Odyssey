## Vec metotları

| Metot | Ne yapar |
|---|---|
| `Vec::new()`, `vec![1, 2]`, `vec![0; 5]` | Oluşturur |
| `Vec::with_capacity(n)` | Yer ayırarak oluşturur |
| `push(x)`, `pop()` | Sona ekler, sondan çıkarır |
| `insert(i, x)`, `remove(i)` | Araya ekler, siler (kalanlar kayar) |
| `len()`, `is_empty()`, `capacity()` | Boyut bilgisi |
| `contains(&x)` | Var mı |
| `sort()`, `reverse()`, `dedup()` | Sıralar, ters çevirir, ardışık tekrarları atar |
| <code>retain(&#124;x&#124; ...)</code> | Koşula uymayanı siler |
| `extend(...)`, `append(&mut o)` | Sonuna ekler |
| `truncate(n)`, `clear()` | Kısaltır, boşaltır |

`retain`'e verilen `|x| ...` adsız, tek satırlık bir fonksiyondur. Ayrıntısı bir sonraki modülde.

## Ondalıklıları sıralamak

`f64` için `sort()` çalışmaz, çünkü `NaN` karşılaştırılamaz:

```rust
fn main() {
    let mut values = vec![2.5, -1.0, 9.75];
    values.sort_by(|a: &f64, b: &f64| a.total_cmp(b));
    println!("{:?}", values);
}
```

```text
[-1.0, 2.5, 9.75]
```

## Maliyetler

| İşlem | Maliyet |
|---|---|
| `push`, `pop` | Hızlı |
| `v[i]` | Hızlı |
| `insert(0, x)`, `remove(0)` | Yavaş: Bütün elemanlar kayar |
| `contains` | Yavaş: Tek tek bakar |

Başta çok ekleme ya da çıkarma yapacaksan `VecDeque`, çok arama yapacaksan `HashSet`.

## Birden çok tür

`Vec` tek tür tutar. Farklı türler için enum kullanılır:

```rust
#[derive(Debug)]
enum Cell {
    Number(i32),
    Text(String),
}

fn main() {
    let row = vec![Cell::Number(7), Cell::Text(String::from("hi"))];
    println!("{:?}", row);
}
```

```text
[Number(7), Text("hi")]
```
