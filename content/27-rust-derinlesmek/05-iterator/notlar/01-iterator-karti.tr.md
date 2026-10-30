## Uyarlayıcılar (tembel)

| Metot | Örnek | Sonuç |
|---|---|---|
| `map` | <code>[1,2].map(&#124;x&#124; x*2)</code> | `2, 4` |
| `filter` | <code>filter(&#124;x&#124; **x &gt; 1)</code> | `2` |
| `filter_map` | <code>filter_map(&#124;s&#124; s.parse().ok())</code> | Yalnızca `Some`'lar |
| `take`, `skip` | `take(2)`, `skip(1)` | İlkler, kalanlar |
| `take_while`, `skip_while` | <code>take_while(&#124;x&#124; **x &lt; 3)</code> | Koşul sürdükçe |
| `enumerate` | `enumerate()` | `(0, a), (1, b)` |
| `zip` | `a.iter().zip(b.iter())` | `(a0, b0), ...` |
| `chain` | `a.iter().chain(b.iter())` | Arka arkaya |
| `rev` | `rev()` | Ters |
| `flat_map` | <code>flat_map(&#124;l&#124; l.chars())</code> | Düzleşir |
| `windows`, `chunks` | `v.windows(2)` | Dilimde: Kayan pencere |
| `cloned`, `copied` | `iter().copied()` | `&T`'den `T` |

## Tüketiciler

| Metot | Döner |
|---|---|
| `collect()` | Hedef koleksiyon |
| `sum()`, `product()` | Toplam, çarpım |
| `count()` | `usize` |
| `max()`, `min()` | `Option<T>` |
| `max_by_key(f)`, `min_by_key(f)` | `Option<T>` |
| `find(f)`, `position(f)` | `Option` |
| `any(f)`, `all(f)` | `bool` |
| `fold(a, f)` | Birikim |
| `for_each(f)` | `()` |
| `last()`, `nth(n)` | `Option<T>` |

## collect hedefleri

```rust
use std::collections::BTreeMap;

fn main() {
    let joined: String = vec!["a", "b"].concat();
    let total: i32 = [1, 2].iter().sum();
    let map: BTreeMap<char, usize> = "ab".chars().zip(0..).collect();
    let (even, odd): (Vec<i32>, Vec<i32>) = (1..5).partition(|x| x % 2 == 0);
    println!("{joined} {total} {:?} {:?} {:?}", map, even, odd);
}
```

```text
ab 3 {'a': 0, 'b': 1} [2, 4] [1, 3]
```

`sum` da hedef türü ister: `let s: i32 = ...sum();`.
