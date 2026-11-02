| Question | Test | scipy |
|---|---|---|
| Two independent groups | Mann–Whitney U | `stats.mannwhitneyu(b, a)` |
| Paired measurements | Wilcoxon signed-rank | `stats.wilcoxon(before, after)` |
| Three or more groups | Kruskal–Wallis | `stats.kruskal(*groups)` |
| Ranks | — | `stats.rankdata(x)` |

## The common language effect size

$U / (n_A n_B)$: the probability that a random B value is larger than a
random A value. 0.5 means no difference.

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

## Choosing

- Bell-shaped data, a question about the mean → t-test / ANOVA.
- A small sample, very skewed data or outliers → a rank-based test.
- With a large sample and a question about the mean (revenue) → the t-test
  or the bootstrap.
- For one-sided questions all of them take `alternative="greater"` /
  `"less"`.
