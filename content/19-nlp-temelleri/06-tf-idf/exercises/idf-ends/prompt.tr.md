`idf_ends(k)` taleplerde IDF'i **en düşük** `k` kelimeyi ve **en yüksek** `k`
kelimeyi döndürsün: `[düşükler, yüksekler]`, her ikisi de IDF'e göre küçükten
büyüğe. Eşit IDF'lerde sıra karışmasın diye `np.argsort(...,
kind="stable")` kullan.

**Beklenen çıktı:**

```
the, my, for, order, ord
watiing, webstie, whree, wlil, wokring
```
