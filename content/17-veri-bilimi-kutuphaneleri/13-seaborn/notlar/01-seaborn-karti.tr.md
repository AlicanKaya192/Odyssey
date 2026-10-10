## Fonksiyonlar

| Soru | Alan düzeyi (`ax=`) | Şekil düzeyi (paneller) |
|---|---|---|
| Dağılım | `histplot`, `kdeplot`, `ecdfplot` | `displot` |
| Kategori | `boxplot`, `violinplot`, `barplot`, `countplot`, `stripplot` | `catplot` |
| İlişki | `scatterplot`, `lineplot` | `relplot` |
| Regresyon | `regplot` | `lmplot` |
| Tablo | `heatmap` | `clustermap` |
| Hepsi birden | — | `pairplot`, `jointplot` |

## Ortak parametreler

| Yazım | Ne yapar |
|---|---|
| `data=df, x="a", y="b"` | DataFrame ve sütun adları |
| `hue="c"` | renge göre grupla |
| `style="c"`, `size="c"` | işarete / boyuta göre |
| `col="c"`, `row="c"`, `col_wrap=3` | panellere böl (şekil düzeyi) |
| `order=[...]`, `hue_order=[...]` | kategori sırası |
| `estimator="sum"`, `errorbar=None` | barplot / lineplot hesabı |
| `stat="density"`, `common_norm=False` | farklı boyutlu grupları karşılaştır |
| `height=2.5, aspect=1.2` | panel boyutu (şekil düzeyi) |
| `palette="colorblind"` | renk paleti |

## Görünüm

| Yazım | Ne yapar |
|---|---|
| `sns.set_theme(style="whitegrid")` | genel stil (kalıcı) |
| `sns.set_context("talk")` | yazı ve çizgi boyu (sunum için) |
| `sns.despine()` | üst ve sağ çerçeveyi kaldır |
| `grid.set_titles("{col_name}")` | panel başlıkları |
| `grid.set_axis_labels("x", "y")` | panel eksen adları |
| `grid.figure.savefig("a.png")` | şekil düzeyini kaydet |

## Tuzaklar

| Belirti | Sebep |
|---|---|
| Çubuk boyu toplamdan küçük | `barplot` ortalama çiziyor |
| Veride olmayan düzgün çizgi | `lineplot` aynı x'leri ortalıyor |
| Küçük grup görünmüyor | ham sayı; `stat="density"` |
| `is a figure-level function and does not accept the ax= parameter` | şekil düzeyi `ax` almaz; uyarı verip yeni şekil açar |
| `load_dataset` takıldı | internet gerekiyor |
| Kategoriler alfabetik | `order=` ver |
