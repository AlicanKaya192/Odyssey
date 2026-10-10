`top_chart(channels, sales)` kanal başına toplam satışı hesaplasın (pandas
`groupby`), **büyükten küçüğe** sıralasın ve yatay çubuk grafik çizsin:
en büyük çubuk `"tab:blue"`, diğerleri `"lightgray"`, değerler çubuğun
ucunda (`bar_label`). `barh` ilk elemanı alta koyar; en büyüğün üstte olması
için sıralı listeyi **ters** ver. `top.png` olarak kaydedip şekli kapatsın.
Şunu döndürsün:

- `"order"`: büyükten küçüğe kanallar
- `"labels"`: `bar_label` yazıları (çizim sırasıyla)
- `"highlight"`: vurgulanan kanal

**Beklenen çıktı:**

```
['web', 'store', 'phone']
['2', '9', '10']
web
```
