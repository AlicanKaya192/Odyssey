Bir taramanın bulgu puanları bir liste. `cvss_band` fonksiyonu başlangıç
kodunda hazır.

`band_summary(scores)` fonksiyonunu yaz: beş şiddetin **hepsini** içeren,
şu sırada bir sözlük döndürsün: `"None"`, `"Low"`, `"Medium"`, `"High"`,
`"Critical"`. Değerler o şiddette kaç bulgu olduğu; hiç yoksa `0`.

**Beklenen çıktı:**

```
None 1
Low 1
Medium 1
High 2
Critical 2
```
