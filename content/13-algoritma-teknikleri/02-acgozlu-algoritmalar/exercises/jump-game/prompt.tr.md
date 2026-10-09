`can_reach_end(jumps)` fonksiyonunu yaz: `jumps[i]`, `i` konumundan en fazla
kaç adım ileri atlayabileceğin. 0. konumdan başlayıp son konuma ulaşabiliyorsan
`True` döndürsün.

**Açgözlü:** şimdiye kadar ulaşılabilen en uzak konumu (`farthest`) tut.
Bir konum `farthest`'ın ötesindeyse oraya hiç gelinemez; değilse
`farthest = max(farthest, i + jumps[i])`.

- `[2, 3, 1, 1, 4]` → `True`, `[3, 2, 1, 0, 4]` → `False`

Son satır 300 000 konumluk bir listede; her konumdan bütün atlayışları
işaretleyen çözüm süre sınırına takılır.

**Beklenen çıktı:**

```
True
False
True
```
