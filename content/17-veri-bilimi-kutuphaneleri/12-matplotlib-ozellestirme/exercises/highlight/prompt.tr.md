`highlight(names, values, target)` yatay çubuk grafiği çizsin: bütün çubuklar
`"lightgray"`, yalnızca `target` adlı çubuk `"tab:blue"`. Değerleri çubukların
ucuna yazsın (`ax.bar_label`), üst ve sağ çerçeveyi kaldırsın
(`ax.spines[["top", "right"]].set_visible(False)`). `bars.png` olarak
kaydedip şekli kapatsın. Şunu döndürsün:

- `"colors"`: çubuk renkleri, `matplotlib.colors.to_hex` ile
- `"labels"`: `bar_label` yazıları
- `"spines"`: üst ve sağ çerçevenin görünürlüğü `[üst, sağ]`

**Beklenen çıktı:**

```
['#d3d3d3', '#d3d3d3', '#1f77b4']
['65', '95', '240'] [False, False]
```
