## İskelet

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn name_says_the_behavior() {
        let input = 2;
        let result = double(input);
        assert_eq!(result, 4);
    }
}
```

Hazırla, çalıştır, doğrula. Test adı davranışı anlatır: `empty_list_gives_none`.

## Yardımcılar

| İş | Yazım |
|---|---|
| Eşit | `assert_eq!(a, b, "mesaj")` |
| Eşit değil | `assert_ne!(a, b)` |
| Doğru | `assert!(k)` |
| Ondalık | `assert!((a - b).abs() < 1e-9)` |
| Belirli hata | `assert!(matches!(r, Err(E::Bad)))` |
| Yalnızca debug | `debug_assert!(k)` |

`f64`'ü `==` ile karşılaştırma: `0.1 + 0.2 != 0.3`.

## Ne test etmeli?

| Soru | Örnek |
|---|---|
| Olağan | Normal girdi |
| Sınır | 0, 1, boş, en büyük |
| Hata | Geçersiz girdi hangi hatayı veriyor |
| Değişmez | Sırala, sonra sıralı mı |
| Regresyon | Bulunan her hata için bir test |

## Clippy'den sık öneriler

| Kod | Öneri |
|---|---|
| `for i in 0..v.len()` | `for x in &v` |
| `x == true` | `x` |
| `return x;` sonda | `x` |
| `v.len() == 0` | `v.is_empty()` |
| `&Vec<T>` parametre | `&[T]` |
| `&String` parametre | `&str` |
| `.clone()` gereksiz | Sil |
