## Adapters (lazy)

| Method | Example | Result |
|---|---|---|
| `map` | <code>[1,2].map(&#124;x&#124; x*2)</code> | `2, 4` |
| `filter` | <code>filter(&#124;x&#124; **x &gt; 1)</code> | `2` |
| `filter_map` | <code>filter_map(&#124;s&#124; s.parse().ok())</code> | Only the `Some`s |
| `take`, `skip` | `take(2)`, `skip(1)` | The first ones, the rest |
| `take_while`, `skip_while` | <code>take_while(&#124;x&#124; **x &lt; 3)</code> | While the condition holds |
| `enumerate` | `enumerate()` | `(0, a), (1, b)` |
| `zip` | `a.iter().zip(b.iter())` | `(a0, b0), ...` |
| `chain` | `a.iter().chain(b.iter())` | One after the other |
| `rev` | `rev()` | Reversed |
| `flat_map` | <code>flat_map(&#124;l&#124; l.chars())</code> | Flattened |
| `windows`, `chunks` | `v.windows(2)` | On slices: a sliding window |
| `cloned`, `copied` | `iter().copied()` | `T` from `&T` |

## Consumers

| Method | Returns |
|---|---|
| `collect()` | The target collection |
| `sum()`, `product()` | Sum, product |
| `count()` | `usize` |
| `max()`, `min()` | `Option<T>` |
| `max_by_key(f)`, `min_by_key(f)` | `Option<T>` |
| `find(f)`, `position(f)` | `Option` |
| `any(f)`, `all(f)` | `bool` |
| `fold(a, f)` | A gathering |
| `for_each(f)` | `()` |
| `last()`, `nth(n)` | `Option<T>` |

## collect targets

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

`sum` also wants a target type: `let s: i32 = ...sum();`.
