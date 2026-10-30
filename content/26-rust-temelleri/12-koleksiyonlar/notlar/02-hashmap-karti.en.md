## HashMap methods

| Method | What it does | Returns |
|---|---|---|
| `insert(k, v)` | Adds or overwrites | The old value, `Option` |
| `get(&k)` | Looks up | `Option<&V>` |
| `get_mut(&k)` | Looks up to change | `Option<&mut V>` |
| `remove(&k)` | Deletes | `Option<V>` |
| `contains_key(&k)` | Whether it exists | `bool` |
| `len()`, `is_empty()` | Size | |
| `keys()`, `values()` | Walks | iterator |
| `entry(k)` | Gives the place | `Entry` |

## entry patterns

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

| Written | When |
|---|---|
| `.or_insert(0)` | This value if absent |
| `.or_default()` | The type's default if absent |
| `.or_insert_with(Vec::new)` | Compute if absent |

To gather several values under a key, use `HashMap<K, Vec<V>>` and `.or_default().push(x)`.

## Which types can be keys?

A key type must provide the `Eq` and `Hash` traits. Integers, `char`, `bool`, `String` and `&str` can. **`f64` cannot**, because `NaN` is not equal to itself. For your own struct use `#[derive(PartialEq, Eq, Hash)]`.

## HashMap or BTreeMap?

| Question | Choice |
|---|---|
| Order does not matter, speed does | `HashMap` |
| Sorted walking or range queries are needed | `BTreeMap` |
| Output must be the same on every run | `BTreeMap` or sort |
