## Forms

| Job | Written |
|---|---|
| A single expression | <code>&#124;x&#124; x + 1</code> |
| With types | <code>&#124;x: i32&#124; -&gt; i32 { x + 1 }</code> |
| No parameters | <code>&#124;&#124; 42</code> |
| Move ownership | <code>move &#124;x&#124; x + y</code> |
| Parameter, reading | `fn f<F: Fn(i32) -> i32>(g: F)` |
| Parameter, changing | `fn f<F: FnMut()>(mut g: F)` |
| Parameter, consuming | `fn f<F: FnOnce() -> String>(g: F)` |
| Short form | `fn f(g: impl Fn(i32) -> i32)` |
| Return | `fn f() -> impl Fn(i32) -> i32` |

## Which to ask for?

| Job | Bound |
|---|---|
| `g()` will be called once | `FnOnce` |
| Called many times, state may change | `FnMut` |
| Many times, through a shared reference | `Fn` |

Standard library examples: `Option::map` is `FnOnce`, `Iterator::map` is `FnMut`.

## Where they are used

```rust
fn main() {
    let doubled = Some(4).map(|x| x * 2);
    let fallback = None.unwrap_or_else(|| 7);
    let mut words = vec!["pear", "fig"];
    words.sort_by_key(|w| w.len());
    let mut list = vec![1, 2, 3, 4];
    list.retain(|n| n % 2 == 0);
    println!("{:?} {} {:?} {:?}", doubled, fallback, words, list);
}
```

```text
Some(8) 7 ["fig", "pear"] [2, 4]
```

## Errors

| Code | Meaning | Fix |
|---|---|---|
| `E0308` | Another type on the second call | Use one type |
| `E0373` | The closure outlives a local | `move` |
| `E0382` | A consuming closure called twice | `clone` or a single call |
| `E0596` | `mut` is missing | `let mut f = ...` |
| `E0525` | `Fn` wanted, `FnOnce` given | Loosen the bound |
