## İskelet

```rust
struct Steps {
    current: u32,
    end: u32,
}

impl Iterator for Steps {
    type Item = u32;

    fn next(&mut self) -> Option<u32> {
        if self.current >= self.end {
            return None;
        }
        self.current += 1;
        Some(self.current)
    }
}
```

## IntoIterator üç biçim

| Yazım | Eleman | Kaynak |
|---|---|---|
| `for x in shelf` | `Book` | `impl IntoIterator for Shelf` |
| `for x in &shelf` | `&Book` | `impl IntoIterator for &Shelf` |
| `for x in &mut shelf` | `&mut Book` | `impl IntoIterator for &mut Shelf` |

İç listeye havale edilir: `self.books.iter()`, `self.books.iter_mut()`, `self.books.into_iter()`.

## Sık hatalar

| Belirti | Sebep |
|---|---|
| Program bitmiyor | Sonsuz iterator'da `take` yok |
| İlk eleman atlanıyor | `next`'te önce artırıp sonra döndürmek yanlış sırada |
| Son eleman eksik | Bitiş koşulu `>=` yerine `>` ya da tersi |
| `E0207`, `E0106` | `'a` eksik |

Bitiş koşulunu sınır değerleriyle dene: Boş aralık, tek eleman.

## Uzunluk ipucu

`size_hint` "kaç eleman kaldı" bilgisini verir; `Vec` `collect` sırasında yer ayırmak için kullanır. Varsayılanı yeterlidir. Tam sayı biliyorsan `ExactSizeIterator` da yazılır, `.len()` kazandırır.
