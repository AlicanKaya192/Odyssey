## Vec methods

| Method | What it does |
|---|---|
| `Vec::new()`, `vec![1, 2]`, `vec![0; 5]` | Creates |
| `Vec::with_capacity(n)` | Creates with reserved room |
| `push(x)`, `pop()` | Adds to the end, removes from the end |
| `insert(i, x)`, `remove(i)` | Inserts, removes (the rest shift) |
| `len()`, `is_empty()`, `capacity()` | Size information |
| `contains(&x)` | Whether it exists |
| `sort()`, `reverse()`, `dedup()` | Sorts, reverses, removes adjacent repeats |
| <code>retain(&#124;x&#124; ...)</code> | Removes what fails a condition |
| `extend(...)`, `append(&mut o)` | Adds to the end |
| `truncate(n)`, `clear()` | Shortens, empties |

The `|x| ...` given to `retain` is a nameless one-line function. Details come in the next module.

## Sorting decimals

`sort()` does not work for `f64`, because `NaN` cannot be compared:

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

## Costs

| Operation | Cost |
|---|---|
| `push`, `pop` | Fast |
| `v[i]` | Fast |
| `insert(0, x)`, `remove(0)` | Slow: all elements shift |
| `contains` | Slow: it looks one by one |

For much adding or removing at the front use `VecDeque`; for much searching use `HashSet`.

## Several types

A `Vec` holds one type. For different types use an enum:

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
