`compare(a, b)` yan yana iki alan açsın (`plt.subplots(1, 2, ...)`), soldakine
`a`'yı, sağdakine `b`'yi çizsin ve iki alanın **aynı y eksenini** kullanmasını
sağlasın (`sharey=True`). `compare.png` olarak kaydedip şekli kapatsın.
`[sınırlar_aynı_mı, [alt, üst]]` döndürsün; sınırlar soldaki alanın
`get_ylim()`'i, 1 basamağa yuvarlı.

**Beklenen çıktı:**

```
[True, [4.5, 125.5]]
```
