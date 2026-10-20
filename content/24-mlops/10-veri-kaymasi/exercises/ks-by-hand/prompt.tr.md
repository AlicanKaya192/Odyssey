İki örneklem arasındaki KS istatistiğini hesaplayan `ks_statistic(a, b)` fonksiyonunu yaz:

- İki listeyi sırala.
- İki listedeki her farklı değer `x` için, her listede `x`'ten küçük ya da eşit değerlerin payını bul (`bisect.bisect_right(liste, x) / len(liste)`).
- İki pay arasındaki en büyük farkı üç basamağa yuvarlayıp döndür.

**Beklenen çıktı:**

```
0
0.4
0.667
```
