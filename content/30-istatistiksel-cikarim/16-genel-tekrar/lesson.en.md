# Overall Review

You have reached the end of the Statistical Inference module. Starting from
a sample differing from its population, through confidence intervals,
hypothesis tests, effect size, power analysis and the Bayesian view, you have
seen every tool needed to read an A/B test. This section walks the path once
more; at the end there is an A/B analysis from start to finish.

<figure class="fig">
  <div class="flow">
    <span class="node">Sample<br><small>00–04</small></span><span class="arrow">→</span>
    <span class="node">Interval<br><small>05</small></span><span class="arrow">→</span>
    <span class="node">Test<br><small>06–12</small></span><span class="arrow">→</span>
    <span class="node">Effect and power<br><small>13–14</small></span><span class="arrow">→</span>
    <span class="node acc">Bayes<br><small>15</small></span>
  </div>
  <figcaption>The module's path: first see the uncertainty, then measure it, test, state the size and finally look with another eye.</figcaption>
</figure>

## 1. Samples and estimation (Sections 0–4)

| Concept | To remember |
|---|---|
| Population and sample | a parameter belongs to the population, a statistic to the sample; every sample gives a different answer |
| Biased sample | making it bigger does not fix the bias |
| Centre and spread | the mean is sensitive to outliers, the median is not; n − 1 in the deviation |
| Distributions | binomial (how many successes), Poisson (how many events), normal (bell) |
| Central limit theorem | the distribution of means approaches a bell; later on skewed data |
| Standard error | $s / \sqrt{n}$; doubling precision needs four times the data |

## 2. Confidence intervals (Section 5)

Estimate ± multiplier × standard error. "95%" is the rate at which the method
catches the truth over repeats, not the probability of a single interval.
The t multiplier for small samples, the Wilson interval for rates.

## 3. Hypothesis tests (Sections 6–12)

| Question | Test | scipy / statsmodels |
|---|---|---|
| Two independent means | Welch's t-test | `stats.ttest_ind(b, a, equal_var=False)` |
| Paired measurements | paired t-test | `stats.ttest_rel(before, after)` |
| Two rates | z-test | `proportions_ztest([k_b, k_a], [n_b, n_a])` |
| Small counts | Fisher | `stats.fisher_exact(table)` |
| Distribution / independence | chi-square | `stats.chisquare`, `stats.chi2_contingency` |
| Three or more means | ANOVA + Tukey | `stats.f_oneway`, `stats.tukey_hsd` |
| Skewed data, outliers | rank-based tests | `mannwhitneyu`, `wilcoxon`, `kruskal` |

p answers "if H₀ were true, how often would a result this extreme come up?".
It is not the probability of H₀ and not the size of the effect; with many
comparisons false alarms pile up.

## 4. Effect size and power (Sections 13–14)

- Cohen's d and h give the difference on a standard scale; the risk
  difference, relative risk and odds ratio describe rates. The relative risk
  is written with the base rate.
- Power = the probability of catching a real effect. Given three of effect,
  α, power and n, the fourth is found with `solve_power`; n is inversely
  proportional to the square of the effect.
- Results that come out significant at low power exaggerate the effect.

## 5. The Bayesian view (Section 15)

Beta prior + data → Beta posterior; P(B > A), the credible interval and the
expected loss are the numbers a decision maker asks for directly. The prior
is chosen in advance with a justification.

## An A/B test from start to finish

The order is always the same: **plan first, then data.**

**1. Plan.** The base buying rate is 11.4%; the team considers a rise to at
least 13.0% worthwhile. How many people are needed, and what is the decision
rule?

```python
import numpy as np
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize

h = proportion_effectsize(0.130, 0.114)
n_plan = NormalIndPower().solve_power(effect_size=h, power=0.8, alpha=0.05)
print(int(np.ceil(n_plan)))
```

```text
6562
```

The plan: 6600 people per group (a little margin), a two-sided z-test,
α = 0.05, a practical threshold of 1 point. These are written before the
test starts.

**2. Analysis.** The test is over:

```python
from statsmodels.stats.proportion import confint_proportions_2indep
from statsmodels.stats.proportion import proportions_ztest
from ab_data import make_checkout_test

shop = make_checkout_test(n=6600, seed=601)
k = shop.groupby("group")["bought"].sum()
rate_a, rate_b = k["A"] / 6600, k["B"] / 6600
p = proportions_ztest([k["B"], k["A"]], [6600, 6600])[1]
low, high = confint_proportions_2indep(k["B"], 6600, k["A"], 6600)
print(round(rate_a, 4), round(rate_b, 4))
print(f"{p:.1e}")
print(round(low, 4), round(high, 4))
```

```text
0.1106 0.1315
2.3e-04
0.0098 0.032
```

**3. Report.** "With the new button the buying rate was 13.15%
instead of 11.06%: a difference of 2.1 points (95%
confidence interval 0.98 – 3.20 points, p =
2.3e-04). The difference is very likely real. Since the lower end of
the interval is just below the 1-point threshold, we cannot say for sure
that the threshold was cleared."

This report uses everything you saw in the module: the plan (power), the
test (p), the interval (uncertainty), the effect (the point difference) and
the practical threshold. A single p-value replaces none of these.
