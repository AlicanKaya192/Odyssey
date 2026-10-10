`grouped_bars(names, a, b)` her kategoride iki seriyi **yan yana** çizsin:
`x = np.arange(len(names))`, birinci seri `x - 0.2`'ye, ikinci `x + 0.2`'ye,
genişlik `0.4`. İşaretleri `ax.set_xticks(x, names)` ile ortala. Şekli
kapatıp `[çubuk_sayısı, çubuk_ortaları]` döndürsün; çubuk ortası
`p.get_x() + p.get_width() / 2`, 1 basamağa yuvarlı, `ax.patches` sırasıyla.
Başlangıç kodunda iki seri aynı yere çiziliyor.

**Beklenen çıktı:**

```
[6, [-0.2, 0.8, 1.8, 0.2, 1.2, 2.2]]
```
