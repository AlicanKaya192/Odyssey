`factorize(n)` fonksiyonunu yaz: `n`'in asal çarpanlarını küçükten büyüğe,
tekrarlarıyla birlikte liste olarak döndürsün (`360` → `[2, 2, 2, 3, 3, 5]`).

`d`'yi 2'den başlat; `d` böldükçe böl ve listeye ekle. Yalnızca `d * d <= n`
iken dene: döngü bitince `n` hâlâ 1'den büyükse o da asal bir çarpan. Son
satırdaki milyar büyüklüğündeki asalda `n`'e kadar denemek süreye takılır.

**Beklenen çıktı:**

```
[2, 2, 2, 3, 3, 5]
[97]
[1000000007]
```
