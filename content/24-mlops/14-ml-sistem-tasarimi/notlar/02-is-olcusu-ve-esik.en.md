With the model unchanged, a different threshold changes the decision, and
a different decision changes the profit.

## The lesson's measurement (1000 customers, 297 churned)

| Threshold | Offers | Profit | Accuracy |
|---|---|---|---|
| 0.2 | 474 | 2166 | 0.733 |
| 0.31 | 352 | 2254 | 0.797 |
| 0.4 | 272 | 2150 | 0.821 |
| 0.5 | 204 | 1806 | 0.813 |

- The threshold with the largest profit is 0.31; the one with the largest
  accuracy is 0.4.
- Offering everyone: 1000 offers, 346 units.

## Comparing the fallback

| What runs | Offers | Profit |
|---|---|---|
| The model (threshold 0.31) | 352 | 2254 |
| The rule (`support_calls >= 2`) | 172 | 1066 |
| Nothing | 0 | 0 |

## The calculation

- For every customer offered: `18 - 5 = 13` if they would churn, `-5` if
  they would stay.
- Profit = the sum of these values.

## Don't

- Don't leave the threshold at the default 0.5; choose it by the measure.
- Don't report the profit on the set where you chose the threshold and
  stop there; confirm it on another period.
