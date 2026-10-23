`dates_in(text, policy)` metindeki `GG/GG/YYYY` biçimli bütün tarihleri
(iki rakam, iki rakam, dört rakam, kelime sınırlı) sırayla bulsun ve her
biri için bir sonuç döndürsün:

- `policy` `"US"` ise ilk sayı ay, `"day-first"` ise ilk sayı gün.
- `policy` `None` ise: iki sayı da 12 ya da daha küçük ve farklıysa
  `"needs_clarification"`; değilse 12'den büyük olan gündür (eşitse fark
  etmez).
- Sonuç `"2026-03-04"` biçiminde tarih; böyle bir gün yoksa (13. ay,
  31 Şubat) `"rejected"`.

**Beklenen çıktı:**

```
['2026-03-04', 'rejected']
['needs_clarification', '2026-04-13']
```
