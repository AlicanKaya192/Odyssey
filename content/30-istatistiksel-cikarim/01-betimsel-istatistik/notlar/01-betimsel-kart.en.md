| Measure | pandas | NumPy | Outliers |
|---|---|---|---|
| Mean | `x.mean()` | `np.mean(x)` | sensitive |
| Median | `x.median()` | `np.median(x)` | robust |
| Mode | `x.mode()[0]` | — | — |
| Variance | `x.var()` | `np.var(x, ddof=1)` | sensitive |
| Standard deviation | `x.std()` | `np.std(x, ddof=1)` | sensitive |
| Percentile | `x.quantile(0.95)` | `np.percentile(x, 95)` | robust |
| Interquartile range (IQR) | `x.quantile(0.75) - x.quantile(0.25)` | `scipy.stats.iqr(x)` | robust |
| All at once | `x.describe()` | `scipy.stats.describe(x)` | — |

## The ddof trap

- pandas `var()` and `std()`: default `ddof=1` (divides by $n-1$).
- NumPy `var()` and `std()`: default `ddof=0` (divides by $n$).
- If you estimate the population's spread from a sample, use `ddof=1`.

## Formulas

$$\bar{x} = \dfrac{1}{n}\sum_{i=1}^{n} x_i \qquad s^2 = \dfrac{1}{n-1}\sum_{i=1}^{n}(x_i - \bar{x})^2 \qquad z = \dfrac{x - \bar{x}}{s}$$

## Outlier rules

- In bell-shaped data: $\lvert z \rvert > 3$.
- In skewed data: above $Q_3 + 1.5 \cdot IQR$ or below $Q_1 - 1.5 \cdot IQR$.
- Before deleting an outlier, look at its cause; write in the report what
  you did.
