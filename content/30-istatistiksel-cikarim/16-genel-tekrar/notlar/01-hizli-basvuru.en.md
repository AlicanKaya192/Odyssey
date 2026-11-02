## What am I asking, what do I use?

| Question | Tool |
|---|---|
| How uncertain is a single value? | standard error, confidence interval (`stats.t.interval`, `proportion_confint`) |
| Are two means different? | Welch `ttest_ind(..., equal_var=False)`; if paired `ttest_rel` |
| Are two rates different? | `proportions_ztest`, interval `confint_proportions_2indep` |
| The counts are very small | `fisher_exact` |
| Are categories independent? | `chi2_contingency`, strength `stats.contingency.association` (Cramér's V) |
| Three or more groups | `f_oneway`, then `tukey_hsd` |
| Skewed data, outliers | `mannwhitneyu`, `wilcoxon`, `kruskal` |
| How big is the difference? | Cohen's d, Cohen's h, risk difference, relative risk, η² |
| How many people are needed? | `TTestIndPower` / `NormalIndPower` + `solve_power` |
| The probability B is better | Beta posterior, draw and `(draw_b > draw_a).mean()` |

## Numbers

- For a 95% interval with a large sample the multiplier ≈ 1.96.
- The standard error is $s / \sqrt{n}$; it halves when n quadruples.
- Cohen's guide (d, h): 0.2 small, 0.5 medium, 0.8 large.
- The usual design: α = 0.05, power = 0.8.

## The skeleton of a report

1. The plan: metric, base rate, smallest worthwhile effect, n, duration,
   test, threshold.
2. The two groups' values and ns.
3. The difference and its 95% interval, in the metric's own unit.
4. The p-value (and a multiple comparison correction if needed).
5. The comparison with the practical threshold and the decision.

## Red flags

- Changing the test, the threshold or the prior after seeing the result.
- Saying "not significant" = "no effect".
- Reporting only the relative increase.
- Looking at 20 metrics and picking the significant one.
- Believing a big effect from a small test.
