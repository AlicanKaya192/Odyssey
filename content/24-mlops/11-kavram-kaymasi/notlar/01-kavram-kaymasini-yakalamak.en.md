Concept drift can't be seen by looking at the inputs; it is seen when the
labels arrive.

## The lesson's measurements

| Month | Expected churn | Happened | Difference |
|---|---|---|---|
| 0 | 0.277 | 0.297 | -0.020 |
| 3 | 0.425 | 0.410 | 0.015 |
| 4 | 0.504 | 0.413 | 0.091 |
| 6 | 0.576 | 0.471 | 0.105 |

The difference grows suddenly in month 4: calibration broke.

## How two weights changed

| Feature | First model | Last window |
|---|---|---|
| `monthly_fee` | 0.87 | 1.89 |
| `support_calls` | 1.02 | 0.24 |

Weights can only be compared with each other if the features are scaled
(`StandardScaler`).

## Signals

- **Calibration:** the average probability given and the rate that
  happened diverge.
- **Accuracy:** accuracy drops although the inputs barely drift.
- **Weights:** a model trained on new data has clearly different weights
  from the old one.

## Don't

- Don't look for concept drift only in the input distribution; PSI doesn't
  measure the relationship.
- Don't compare the weights of unscaled features with each other.
- Don't measure calibration with `predict(...).mean()`; probabilities
  (`predict_proba`) are needed.
