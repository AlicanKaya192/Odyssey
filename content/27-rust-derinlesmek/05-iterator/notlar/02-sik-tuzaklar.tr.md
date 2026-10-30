## Referans kafa karışıklığı

| Yazım | Parametre türü |
|---|---|
| <code>v.iter().map(&#124;x&#124; ...)</code> | `x: &T` |
| <code>v.iter().filter(&#124;x&#124; ...)</code> | `x: &&T` |
| <code>v.into_iter().map(&#124;x&#124; ...)</code> | `x: T` |
| <code>v.into_iter().filter(&#124;x&#124; ...)</code> | `x: &T` |

Tür hatası alınca sorun çoğu zaman burada. `.copied()` ile `&T`'den kurtulabilirsin:

```rust
fn main() {
    let v = vec![1, 2, 3];
    let big: Vec<i32> = v.iter().copied().filter(|x| *x > 1).collect();
    println!("{:?}", big);
}
```

```text
[2, 3]
```

## Tek kullanımlık

Iterator kendini tüketir. İkinci kez gezmek için yenisini oluştur:

```rust
fn main() {
    let v = vec![1];
    let it = v.iter();
    let a: i32 = it.sum();
    let b: i32 = it.sum();
    println!("{a} {b}");
}
```

```text
error[E0382]: use of moved value: `it`
 --> main.rs:5:18
  |
3 |     let it = v.iter();
  |         -- move occurs because `it` has type `std::slice::Iter<'_, i32>`, which does
  not implement the `Copy` trait
4 |     let a: i32 = it.sum();
  |                     ----- `it` moved due to this method call
5 |     let b: i32 = it.sum();
  |                  ^^ value used here after move
  |
note: `std::iter::Iterator::sum` takes ownership of the receiver `self`, which moves
`it`
help: you can `clone` the value and consume it, but this might not be your desired
behavior
  |
4 |     let a: i32 = it.clone().sum();
  |                    ++++++++
```

## Sık kullanılan birleşimler

```rust
fn main() {
    let words = ["apple", "fig", "cherry"];
    let lengths: Vec<usize> = words.iter().map(|w| w.len()).collect();
    let longest = words.iter().max_by_key(|w| w.len());
    let line = words.join(", ");
    let numbers: Vec<i32> = "1 x 3".split(' ').filter_map(|s| s.parse().ok()).collect();
    let sums: Vec<i32> = [1, 2, 3].windows(2).map(|w| w[0] + w[1]).collect();
    println!("{:?} {:?} {line}", lengths, longest);
    println!("{:?} {:?}", numbers, sums);
}
```

```text
[5, 3, 6] Some("cherry") apple, fig, cherry
[1, 3] [3, 5]
```

## Gereksiz collect

| Kötü | İyi |
|---|---|
| `.collect::<Vec<_>>().len()` | `.count()` |
| `.collect::<Vec<_>>().iter()` | Doğrudan devam et |
| <code>filter(&#124;x&#124; ...).next()</code> | <code>find(&#124;x&#124; ...)</code> |
| <code>map(&#124;x&#124; x.clone())</code> | `cloned()` |

`cargo clippy` bunların çoğunu söyler.
