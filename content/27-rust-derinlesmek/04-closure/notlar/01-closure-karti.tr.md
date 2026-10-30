## Yazımlar

| İş | Yazım |
|---|---|
| Tek ifade | <code>&#124;x&#124; x + 1</code> |
| Türlü | <code>&#124;x: i32&#124; -&gt; i32 { x + 1 }</code> |
| Parametresiz | <code>&#124;&#124; 42</code> |
| Sahipliği taşı | <code>move &#124;x&#124; x + y</code> |
| Parametre, okuyan | `fn f<F: Fn(i32) -> i32>(g: F)` |
| Parametre, değiştiren | `fn f<F: FnMut()>(mut g: F)` |
| Parametre, tüketen | `fn f<F: FnOnce() -> String>(g: F)` |
| Kısa yazım | `fn f(g: impl Fn(i32) -> i32)` |
| Döndür | `fn f() -> impl Fn(i32) -> i32` |

## Hangisini istemeli?

| İş | Kısıt |
|---|---|
| `g()` bir kez çağrılacak | `FnOnce` |
| Çok kez çağrılacak, durumu değişebilir | `FnMut` |
| Çok kez, paylaşılan referansla | `Fn` |

Standart kütüphane örnekleri: `Option::map` `FnOnce`, `Iterator::map` `FnMut`.

## Kullanım yerleri

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

## Hatalar

| Kod | Anlamı | Çözüm |
|---|---|---|
| `E0308` | İkinci çağrıda başka tür | Tek tür kullan |
| `E0373` | Closure yerelden uzun yaşıyor | `move` |
| `E0382` | Tüketen closure iki kez çağrıldı | `clone` ya da tek çağrı |
| `E0596` | `mut` eksik | `let mut f = ...` |
| `E0525` | `Fn` istenip `FnOnce` verildi | Kısıtı gevşet |
