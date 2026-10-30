## Result metotları

| Metot | `Ok(v)` için | `Err(e)` için |
|---|---|---|
| `is_ok()`, `is_err()` | `true`, `false` | `false`, `true` |
| `unwrap()` | `v` | Panik |
| `expect("m")` | `v` | Panik, mesajla |
| `unwrap_or(d)` | `v` | `d` |
| `unwrap_or_default()` | `v` | Türün varsayılanı |
| `ok()` | `Some(v)` | `None` |
| `err()` | `None` | `Some(e)` |
| <code>map(&#124;v&#124; ...)</code> | Yeni `Ok` | Aynı `Err` |
| <code>map_err(&#124;e&#124; ...)</code> | Aynı `Ok` | Yeni `Err` |
| `?` | `v` | `Err`'i döndürür |

## Option ile karşılaştırma

| İş | `Option` | `Result` |
|---|---|---|
| Başarı | `Some(v)` | `Ok(v)` |
| Başarısızlık | `None` | `Err(e)` |
| Neden anlatır mı? | Hayır | **Evet** |
| Çeviri | `ok_or(e)` | `ok()` |

Tek bir sebebi olan "yok" için `Option`, sebebi önemli olan başarısızlık için `Result`.

## Birden çok değeri okumak

`collect` `Result` üretebilir: Biri bile hatalıysa ilk hata döner.

```rust
fn numbers(line: &str) -> Result<Vec<i32>, std::num::ParseIntError> {
    line.split_whitespace()
        .map(|t| t.parse::<i32>())
        .collect()
}

fn main() {
    println!("{:?}", numbers("1 2 3"));
    println!("{}", numbers("1 x 3").is_err());
}
```

```text
Ok([1, 2, 3])
true
```

## Ters giden yaygın üç şey

| Belirti | Sebep | Düzeltme |
|---|---|---|
| `the ? operator can only be used...` | Fonksiyon `Result` döndürmüyor | İmzayı değiştir |
| `? couldn't convert the error` | Hata türleri farklı | `map_err` |
| `unused Result` uyarısı | Sonuç görmezden gelinmiş | `match` ya da `?` |
