## Kurmak

| Yazım | Ne verir |
|---|---|
| `fig, ax = plt.subplots()` | bir şekil, bir alan |
| `fig, axes = plt.subplots(2, 3)` | `(2, 3)` dizisi |
| `plt.subplots(1, 3)` | tek boyutlu dizi |
| `plt.subplots(..., squeeze=False)` | her zaman iki boyutlu |
| `plt.subplots(..., sharex=True, sharey=True)` | ortak eksen |
| `plt.subplots(..., figsize=(8, 4), dpi=100)` | inç ve çözünürlük |
| `plt.subplot_mosaic([["a", "b"]])` | adlı alanlar (sözlük) |
| `layout="constrained"` | yazılar çakışmasın |

## Alan (Axes)

| Yazım | Ne yapar |
|---|---|
| `ax.set(title=, xlabel=, ylabel=)` | birden fazla ayar |
| `ax.set_xlim(0, 10)` / `ax.get_xlim()` | eksen sınırları |
| `ax.legend()` | `label=` verilen çizgilerin açıklaması |
| `ax.lines`, `ax.patches` | çizilmiş çizgiler / çubuklar |
| `ax.xaxis`, `ax.yaxis` | tek eksen nesneleri |
| `ax.twinx()` | aynı x, ikinci y ekseni |

## Şekil (Figure)

| Yazım | Ne yapar |
|---|---|
| `fig.suptitle("...")` | bütün şeklin başlığı |
| `fig.savefig("a.png", dpi=200, bbox_inches="tight")` | kaydet |
| `fig.get_size_inches()` | boyut (inç) |
| `fig.axes` | bütün alanlar |
| `plt.close(fig)` / `plt.close("all")` | bırak |

## pyplot ↔ nesne

| pyplot | Nesne |
|---|---|
| `plt.plot(x, y)` | `ax.plot(x, y)` |
| `plt.title("t")` | `ax.set_title("t")` |
| `plt.xlabel("x")` | `ax.set_xlabel("x")` |
| `plt.xlim(0, 5)` | `ax.set_xlim(0, 5)` |
| `plt.gcf()` / `plt.gca()` | `fig` / `ax` |

## Hatalar

| Belirti | Sebep |
|---|---|
| `'Axes' object has no attribute 'xlabel'` | nesnede `set_xlabel`; `xlabel` pyplot'ta |
| `'Text' object is not callable` | `ax.title(...)` yazıldı; `ax.set_title(...)` |
| `'numpy.ndarray' object has no attribute 'plot'` | `axes` dizi; `axes[0]` ile seç |
| `too many indices for array` | `plt.subplots(1, 3)` tek boyutlu |
| İki grafiğin yükseklikleri yanıltıcı | `sharey=True` yok |
| `More than 20 figures have been opened` | döngüde `plt.close(fig)` yok |
| Etiketler üst üste | `layout="constrained"` |
