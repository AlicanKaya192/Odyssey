`positives_per_fold(labels, k)` etiket listesini `StratifiedKFold(k)` ile
(karıştırmadan) bölsün ve her **test** katındaki pozitif (1) sayısını liste
olarak döndürsün. Başlangıç kodu `KFold` kullanıyor; sıralı etiketlerde
pozitiflerin hepsi son kata düşüyor.

**Beklenen çıktı:**

```
[2, 2, 2]
```
