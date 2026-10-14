`pick_version(results)` `[ad, geliştirme, test]` satırlarından geliştirme
başarısı en yüksek olanı seçsin (eşitlikte önce gelen; test sonucuna göre
**seçme**). `[ad, test, açık, ezber şüphesi]` döndürsün: açık
`round(geliştirme - test, 2)`, şüphe açık 0,1'den büyükse `True`.

**Beklenen çıktı:**

```
['v3', 0.75, 0.25, True]
['a', 0.8, 0.0, False]
```
