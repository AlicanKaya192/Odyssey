## Dağılımlar

| Yazım | Ne |
|---|---|
| `stats.norm(loc=, scale=)` | normal |
| `stats.binom(n=, p=)` | binom (n denemede başarı sayısı) |
| `stats.poisson(mu=)` | Poisson (birim zamanda olay sayısı) |
| `stats.expon(scale=)` | üstel (bekleme süresi) |
| `stats.uniform(loc=, scale=)` | düzgün |
| `stats.t(df=)` | t (küçük örneklemde ortalama) |

| Metot | Ne verir |
|---|---|
| `pdf(x)` / `pmf(k)` | yoğunluk / olasılık |
| `cdf(x)` / `sf(x)` | x ve altı / x'in üstü |
| `ppf(q)` / `isf(q)` | cdf'nin tersi / sf'nin tersi |
| `rvs(size=, random_state=)` | örnek |
| `mean()`, `std()`, `interval(0.95)` | dağılımın özellikleri |

## Özet ve testler

| Yazım | Soru |
|---|---|
| `stats.describe(x)` | sayı, ortalama, varyans, çarpıklık, basıklık |
| `stats.sem(x)`, `stats.iqr(x)` | ortalamanın hatası, çeyrekler arası |
| `stats.ttest_ind(a, b, equal_var=False)` | iki bağımsız grubun ortalaması |
| `stats.ttest_rel(önce, sonra)` | aynı kişilerin önce/sonrası |
| `stats.ttest_1samp(x, popmean=50)` | ortalama 50'den farklı mı |
| `res.confidence_interval(0.95)` | farkın güven aralığı |
| `stats.mannwhitneyu(a, b)` | sıralamaya dayalı iki grup (normal değilse) |
| `stats.chi2_contingency(tablo)` | iki kategorik değişken bağımsız mı |
| `stats.pearsonr(x, y)` / `spearmanr` | doğrusal / sıralı ilişki |
| `stats.shapiro(x)` | normal dağılıma uyuyor mu |

## Okurken

| Gördüğün | Anlamı |
|---|---|
| p < 0,05 | sıfır hipotezi altında bu veri **az olası**; fark büyük demek değil |
| p ≥ 0,05 | veri ayırt etmeye **yetmedi**; fark yok demek değil |
| GA sıfırı içeriyor | fark sıfır da olabilir |
| Dar GA | tahmin kesin; geniş GA: daha çok veri gerek |
| Çok test | yanlış alarm beklenir; eşiği test sayısına böl |
