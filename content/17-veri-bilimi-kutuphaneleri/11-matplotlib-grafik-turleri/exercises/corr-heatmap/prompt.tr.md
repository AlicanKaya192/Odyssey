`corr_heatmap(columns)` ad → değerler sözlüğündeki sütunların korelasyon
matrisini hesaplasın (`np.corrcoef(list(columns.values()))`) ve `imshow` ile
ısı haritası çizsin: iki yönlü renk skalası `cmap="RdBu_r"` ve **simetrik**
sınırlar `vmin=-1, vmax=1`. `heat.png` olarak kaydedip şekli kapatsın.
`[sınırlar, matris]` döndürsün: sınırlar `image.get_clim()` (iki `float`),
matris 2 basamağa yuvarlı liste listesi. Başlangıç kodunda sınır verilmediği
için skala matrisin kendi en küçük ve en büyük değerine oturuyor.

**Beklenen çıktı:**

```
[-1.0, 1.0]
[1.0, 0.85, -0.8]
[0.85, 1.0, -0.53]
[-0.8, -0.53, 1.0]
```
