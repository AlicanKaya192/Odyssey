| Soru | Test | scipy |
|---|---|---|
| İki bağımsız grup | Mann–Whitney U | `stats.mannwhitneyu(b, a)` |
| Eşli ölçümler | Wilcoxon işaretli sıra | `stats.wilcoxon(before, after)` |
| Üç ve daha çok grup | Kruskal–Wallis | `stats.kruskal(*groups)` |
| Sıralar | — | `stats.rankdata(x)` |

## Ortak dil etki büyüklüğü

$U / (n_A n_B)$: rastgele bir B değerinin rastgele bir A değerinden büyük
olma olasılığı. 0,5 fark yok demek.

```python
from scipy import stats

a = [42, 55, 61, 48, 70, 52, 66, 58]
b = [68, 75, 81, 72, 90, 77, 85, 79, 900]
u = stats.mannwhitneyu(b, a)
print(round(u.statistic / (len(a) * len(b)), 3), f"{u.pvalue:.1e}")
```

```text
0.986 1.6e-04
```

## Seçim

- Çan biçimli veri, soru ortalama → t-testi / ANOVA.
- Küçük örneklem, çok çarpık veri ya da aykırılar → sıralı test.
- Büyük örneklemde soru ortalama ise (gelir) → t-testi ya da bootstrap.
- Tek yönlü sorular için hepsi `alternative="greater"` / `"less"` alır.
