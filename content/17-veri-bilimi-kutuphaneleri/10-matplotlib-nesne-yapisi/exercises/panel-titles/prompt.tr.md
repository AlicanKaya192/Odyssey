`panel_titles(rows, cols)` `rows × cols` alanlı bir şekil açsın, alanlara sırayla
`"p0"`, `"p1"`, ... başlıklarını versin ve şunu döndürsün:
`[[satır, sütun], [başlıklar]]` (dizinin şekli ve `fig.axes` sırasıyla
başlıklar). Başlangıç kodu `axes.flat` kullanıyor ama `plt.subplots(1, 1)`
tek bir `Axes` döndürdüğü için orada düşüyor. `squeeze=False` her durumda
iki boyutlu dizi verir. Şekli kapat.

**Beklenen çıktı:**

```
[2, 3]
['p0', 'p1', 'p2', 'p3', 'p4', 'p5']
[[1, 1], ['p0']]
```
