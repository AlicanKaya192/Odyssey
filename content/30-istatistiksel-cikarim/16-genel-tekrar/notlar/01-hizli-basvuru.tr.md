## Ne soruyorum, ne kullanırım?

| Soru | Araç |
|---|---|
| Tek bir değer ne kadar belirsiz? | standart hata, güven aralığı (`stats.t.interval`, `proportion_confint`) |
| İki ortalama farklı mı? | Welch `ttest_ind(..., equal_var=False)`; eşliyse `ttest_rel` |
| İki oran farklı mı? | `proportions_ztest`, aralık `confint_proportions_2indep` |
| Sayılar çok küçük | `fisher_exact` |
| Kategoriler bağımsız mı? | `chi2_contingency`, güç `stats.contingency.association` (Cramér's V) |
| Üç ve daha çok grup | `f_oneway`, sonra `tukey_hsd` |
| Çarpık veri, aykırılar | `mannwhitneyu`, `wilcoxon`, `kruskal` |
| Fark ne kadar büyük? | Cohen's d, Cohen's h, risk farkı, göreli risk, η² |
| Kaç kişi gerekir? | `TTestIndPower` / `NormalIndPower` + `solve_power` |
| B'nin daha iyi olma olasılığı | Beta sonsal, örnek çekip `(draw_b > draw_a).mean()` |

## Sayılar

- %95 aralık için büyük örneklemde çarpan ≈ 1,96.
- Standart hata $s / \sqrt{n}$; n dört katına çıkınca yarıya iner.
- Cohen ölçütü (d, h): 0,2 küçük, 0,5 orta, 0,8 büyük.
- Olağan tasarım: α = 0,05, güç = 0,8.

## Raporun iskeleti

1. Plan: metrik, taban oranı, en küçük anlamlı etki, n, süre, test, eşik.
2. İki grubun değerleri ve n'leri.
3. Fark ve %95 aralığı, metriğin kendi biriminde.
4. p değeri (ve gerekiyorsa çoklu karşılaştırma düzeltmesi).
5. Pratik eşikle karşılaştırma ve karar.

## Kırmızı bayraklar

- Sonuca bakıp testi, eşiği ya da önseli değiştirmek.
- "Anlamlı değil" = "etki yok" demek.
- Yalnızca göreli artışı yazmak.
- 20 metriğe bakıp anlamlı çıkanı seçmek.
- Küçük testteki büyük etkiye inanmak.
