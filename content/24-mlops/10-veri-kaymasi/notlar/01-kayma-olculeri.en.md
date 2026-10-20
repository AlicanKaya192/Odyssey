| Measure | What it measures | Range | Note |
|---|---|---|---|
| Difference of means | Shift of the center | Unbounded | Misses changes of shape |
| PSI | How the shares in bins diverge | 0 and above | Rule of thumb: 0.1 / 0.25 |
| KS statistic | Largest distance between cumulative distributions | 0 – 1 | Numeric columns |
| KS p-value | Chance of the difference appearing by luck | 0 – 1 | Everything is "significant" on big samples |
| Category shares | The share of each category | 0 – 1 | PSI's bins in categorical columns |

## PSI step by step

1. Sort the reference and take 9 edges from its deciles.
2. Put every value into its bin with `bisect_left(edges, v)`.
3. Compute each bin's share, at least `0.0001`.
4. `Σ (current - reference) × ln(current / reference)`.

## The lesson's measurement (PSI)

| Month | tenure | monthly_fee | support_calls | usage_hours |
|---|---|---|---|---|
| 0 (another sample) | 0.012 | 0.013 | 0.004 | 0.016 |
| 2 | 0.005 | 0.229 | 0.055 | 0.121 |
| 3 | 0.012 | 0.456 | 0.109 | 0.284 |
| 6 | 0.012 | 1.875 | 0.280 | 1.152 |

In month 3, while the fee showed a "large drift", accuracy was 0.784.

## The same drift, three samples (KS)

| Customers | Statistic | p-value |
|---|---|---|
| 200 | 0.095 | 0.33 |
| 2000 | 0.083 | 2.1e-06 |
| 50,000 | 0.076 | 1.2e-124 |

## Terms

- **Data drift:** the distribution of the inputs changing over time.
- **Reference:** the basis of the comparison; usually the training data.
- **Cumulative distribution:** for every `x`, the share of values less
  than or equal to `x`.
- **p-value:** the chance of a difference this large appearing by luck.
