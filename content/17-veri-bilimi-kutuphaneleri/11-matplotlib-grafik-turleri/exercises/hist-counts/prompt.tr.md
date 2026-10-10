`hist_counts(a, b, bins, low, high)` iki veriyi aynı alanda histogram olarak
çizsin; ikisi de **aynı** kutuları kullansın: `bins=bins`,
`range=(low, high)`. `ax.hist` sayıları da döndürür
(`counts, edges, _ = ax.hist(...)`). Şekli kapatıp
`[a_sayıları, b_sayıları]` döndürsün (her biri `int` listesi). Başlangıç kodu
`range` vermiyor; kutular her veri için başka yerde.

**Beklenen çıktı:**

```
[1, 4, 2, 0]
[0, 1, 4, 3]
```
