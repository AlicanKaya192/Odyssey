## NumPy

| Yazım | Ne |
|---|---|
| `np.array(x, dtype="float32")` | dizi, tür |
| `a.reshape(3, -1)`, `a.T` | şekil, devrik |
| `a[a > 0]`, `a[[0, 2]]` | maske, dizinle seçim (kopya) |
| `a[1:3]` | dilim (görünüm) |
| `a.mean(axis=0)`, `keepdims=True` | sütun ortalaması, şekli koru |
| `np.where(k, a, b)`, `np.select(...)` | koşul |
| `rng = np.random.default_rng(1)` | üreteç |
| `np.linalg.solve(A, b)`, `lstsq` | denklem, en küçük kareler |

## pandas

| Yazım | Ne |
|---|---|
| `df.set_index("a")`, `loc`, `iloc` | indeks, seçim |
| `a.merge(b, on="k", how="left", validate="many_to_one")` | birleştir |
| `pd.concat(parçalar, ignore_index=True)` | alt alta |
| `df.melt(...)`, `df.pivot_table(..., aggfunc="sum")` | şekil |
| `pd.to_datetime(s, format=...)`, `s.dt.month` | tarih |
| `s.resample("ME").sum()`, `rolling(7).mean()` | zamana göre |
| `s.str.strip().str.lower()`, `str.extract(...)` | metin |
| `s.astype("category")`, `pd.cut(...)` | kategori |
| `df.loc[k, "a"] = 1` | değiştir (tek adım) |
| `g.transform("sum")` | grup sonucunu satıra yay |

## Grafik

| Yazım | Ne |
|---|---|
| `fig, ax = plt.subplots(figsize=(6, 3), layout="constrained")` | şekil |
| `ax.plot`, `scatter`, `bar`, `hist`, `boxplot`, `imshow` | türler |
| `ax.set(title=, xlabel=, ylabel=)` | yazılar |
| `fig.savefig("a.png", dpi=200, bbox_inches="tight")`; `plt.close(fig)` | kaydet, bırak |
| `sns.histplot(df, x=, hue=)`, `sns.barplot(..., estimator=)` | seaborn |
| `sns.relplot(..., col=)` | paneller |

## SciPy

| Yazım | Ne |
|---|---|
| `stats.norm(m, s).sf(x)` | x'in üstü olasılığı |
| `stats.ttest_ind(a, b, equal_var=False)` | iki grup |
| `res.confidence_interval()` | farkın aralığı |
| `stats.chi2_contingency(tablo)` | kategorik bağımsızlık |
| `optimize.minimize(f, x0=...)` | en küçükle |
| `optimize.curve_fit(model, x, y, p0=...)` | eğri uydur |
| `interpolate.PchipInterpolator(x, y)` | aşmayan ara değer |

## On kural

1. Etiketle hizalanır; `.values` etiketi atar.
2. Bilgi eklerken `how="left"`, sonra satır sayısını denetle.
3. Tarih metni `format=` ile oku; `NaT` sayısına bak.
4. Döngü yerine sütun işlemi.
5. Değiştirmek için `df.loc[koşul, sütun] = değer`.
6. Önce soru, sonra grafik; çubuk sıfırdan.
7. seaborn'un hangi hesabı yaptığını bil.
8. "Anlamlı değil" ≠ "fark yok"; güven aralığına bak.
9. scipy en küçükler; en büyük için eksi.
10. Rastgelelik varsa tohum yaz.
