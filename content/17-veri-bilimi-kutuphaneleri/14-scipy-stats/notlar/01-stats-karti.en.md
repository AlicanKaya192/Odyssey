## Distributions

| Code | What |
|---|---|
| `stats.norm(loc=, scale=)` | normal |
| `stats.binom(n=, p=)` | binomial (successes in n trials) |
| `stats.poisson(mu=)` | Poisson (events per unit of time) |
| `stats.expon(scale=)` | exponential (waiting time) |
| `stats.uniform(loc=, scale=)` | uniform |
| `stats.t(df=)` | t (a mean in a small sample) |

| Method | Gives |
|---|---|
| `pdf(x)` / `pmf(k)` | density / probability |
| `cdf(x)` / `sf(x)` | x and below / above x |
| `ppf(q)` / `isf(q)` | inverse of cdf / inverse of sf |
| `rvs(size=, random_state=)` | a sample |
| `mean()`, `std()`, `interval(0.95)` | properties of the distribution |

## Summaries and tests

| Code | Question |
|---|---|
| `stats.describe(x)` | count, mean, variance, skewness, kurtosis |
| `stats.sem(x)`, `stats.iqr(x)` | standard error of the mean, interquartile range |
| `stats.ttest_ind(a, b, equal_var=False)` | the means of two independent groups |
| `stats.ttest_rel(before, after)` | the same people before/after |
| `stats.ttest_1samp(x, popmean=50)` | is the mean different from 50 |
| `res.confidence_interval(0.95)` | the difference's confidence interval |
| `stats.mannwhitneyu(a, b)` | two groups by ranks (if not normal) |
| `stats.chi2_contingency(table)` | are two categorical variables independent |
| `stats.pearsonr(x, y)` / `spearmanr` | linear / rank relationship |
| `stats.shapiro(x)` | does it fit a normal distribution |

## When reading

| You see | It means |
|---|---|
| p < 0.05 | this data is **unlikely** under the null hypothesis; not that the difference is big |
| p ≥ 0.05 | the data was **not enough** to tell; not that there is no difference |
| CI contains zero | the difference could be zero |
| Narrow CI | a precise estimate; wide CI: more data needed |
| Many tests | false alarms are expected; divide the threshold by the number of tests |
