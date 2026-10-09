`knapsack(items, capacity)` fonksiyonunu **DP tablosuyla** yaz: `items`
`[değer, ağırlık]` çiftleri, her eşya en fazla bir kez. Kapasiteyi aşmadan
alınabilecek en büyük toplam değeri döndürsün.

`best[i][w] = max(best[i − 1][w], best[i − 1][w − ağırlık] + değer)`
(ikincisi yalnızca eşya sığıyorsa).

Son satırda 100 eşya var: bütün alt kümeleri denemek `2¹⁰⁰`, tablo ise
yalnızca birkaç yüz bin hücre.

**Beklenen çıktı:**

```
220
90
4428
```
