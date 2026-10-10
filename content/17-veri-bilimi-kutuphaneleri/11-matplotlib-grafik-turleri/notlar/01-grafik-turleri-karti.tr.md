## Çizim metotları

| Yazım | Ne çizer |
|---|---|
| `ax.plot(x, y, marker="o")` | çizgi |
| `ax.scatter(x, y, c=z, s=20, cmap="viridis", alpha=0.5)` | dağılım |
| `ax.bar(adlar, değerler)` / `ax.barh(...)` | dikey / yatay çubuk |
| `ax.bar(x, b, bottom=a)` | yığılmış çubuk |
| `ax.bar(x - w/2, a, width=w)` + `ax.bar(x + w/2, b, width=w)` | gruplu çubuk |
| `ax.hist(v, bins=20, range=(0, 80), density=True)` | histogram |
| `ax.boxplot([a, b], tick_labels=["A", "B"])` | kutu |
| `ax.violinplot([a, b])` | keman (dağılımın şekli) |
| `ax.imshow(m, cmap="RdBu_r", vmin=-1, vmax=1)` | ısı haritası |
| `ax.fill_between(x, alt, üst, alpha=0.3)` | bant |
| `ax.errorbar(x, y, yerr=e, fmt="o")` | hata çubuğu |
| `ax.pie(paylar, labels=adlar)` | pasta (yalnızca 2–3 parça) |

## Yardımcılar

| Yazım | Ne yapar |
|---|---|
| `fig.colorbar(nesne, ax=ax, label="...")` | renk skalasının açıklaması |
| `ax.set_xticks(konumlar, etiketler)` | işaret yeri ve yazısı |
| `ax.text(x, y, "metin", ha="center")` | hücreye yazı |
| `ax.legend()` | `label=` verilenlerin açıklaması |

## Renk skalası seçimi

| Veri | Skala |
|---|---|
| Tek yönlü (0'dan büyüğe) | `viridis`, `Blues` |
| İki yönlü (−…+) | `RdBu_r`, `coolwarm` + simetrik `vmin`/`vmax` |
| Kategori | `tab10` (varsayılan döngü) |

## Hatalar

| Belirti | Sebep |
|---|---|
| İki histogram karşılaştırılamıyor | farklı `bins` / `range` |
| Yığılmış çubuklar üst üste biniyor | `bottom=` verilmedi |
| Gruplu çubuklar tek yerde | `x` kaydırılmadı (`x ± w/2`) |
| Isı haritasında sıfır renkli görünüyor | `vmin`/`vmax` simetrik değil |
| Dağılımda yoğunluk görünmüyor | çok nokta; `alpha` |
| `boxplot() got an unexpected keyword argument` | eski kod `labels=`; yenisi `tick_labels=` |
