`count_subsets(items, limit)` fonksiyonunu **ortada buluşma** ile yaz: toplamı
`limit`'i geçmeyen alt küme sayısını (boş küme dahil) döndürsün.

Eşyaları ikiye böl, her yarının bütün alt küme toplamlarını hesapla, birini
sırala ve ötekinin her toplamı için `bisect_right` ile eşleri say. Son
satırdaki 30 eşyada `2³⁰` alt kümeyi tek tek denemek süreye takılır.

**Beklenen çıktı:**

```
6
46879146
```
