Notation: the actual value $y_t$, the forecast $\hat{y}_t$, the error
$e_t = y_t - \hat{y}_t$, the length of the test $n$.

## The formulas

$$\text{MAE} = \frac{1}{n}\sum \lvert e_t \rvert$$

$$\text{RMSE} = \sqrt{\frac{1}{n}\sum e_t^2}$$

$$\text{MAPE} = \frac{100}{n}\sum \left\lvert \frac{e_t}{y_t} \right\rvert$$

$$\text{sMAPE} = \frac{100}{n}\sum \frac{2\,\lvert e_t \rvert}{\lvert y_t \rvert + \lvert \hat{y}_t \rvert}$$

$$\text{MASE} = \frac{\text{MAE}}{\dfrac{1}{T-m}\sum_{t=m+1}^{T} \lvert y_t - y_{t-m} \rvert}$$

The denominator of MASE comes from the **training** data: the mean absolute
difference of each value from the one a season earlier. For a series without a
season, $m = 1$.

## Which one when

| Measure | Unit | Strength | Weakness | When |
|---|---|---|---|---|
| MAE | Unit of the series | Readable; robust to outliers | Not comparable across series | One series, daily reporting |
| RMSE | Unit of the series | Brings out large errors | A few days decide the whole grade | When a big miss is costly |
| MAPE | Percent | Everyone understands it | Undefined at zero; asymmetric | A series always positive and far from zero |
| sMAPE | Percent | Bounded between 0 and 200 | Still sensitive to zero; hard to read | As a competition measure |
| MASE | Unit-free | Defined for every series; has a clear bar | Takes effort to explain | Many series, series with zeros |
| Bias | Unit of the series | Shows the direction | Does not show the size | Always, next to the MAE |

Whichever measure you select by, the model tries to improve **that measure**:

- The forecast that minimises the MAE is the **median**.
- The forecast that minimises the RMSE is the **mean**.
- The forecast that minimises the MAPE sits **below** the median.

On a series with a skewed distribution (few sales most days, many now and
then) the three call for different forecasts. Choose the measure by the
decision, not by habit.

## Code

```python
import numpy as np


def mae(actual, forecast):
    return np.mean(np.abs(actual - forecast))


def rmse(actual, forecast):
    return np.sqrt(np.mean((actual - forecast) ** 2))


def bias(actual, forecast):
    return np.mean(actual - forecast)


def mape(actual, forecast):
    return np.mean(np.abs(actual - forecast) / np.abs(actual)) * 100


def smape(actual, forecast):
    total = np.abs(actual) + np.abs(forecast)
    return np.mean(2 * np.abs(actual - forecast) / total) * 100


def mase(actual, forecast, train, m=1):
    scale = np.mean(np.abs(train[m:] - train[:-m]))
    return mae(actual, forecast) / scale
```

All of them expect numpy arrays: `test.to_numpy()`. If you subtract two pandas
series directly they are aligned **by index**; with different indexes the
result fills up with `NaN`.

The ready-made ones in scikit-learn: `mean_absolute_error`,
`root_mean_squared_error`, `mean_absolute_percentage_error` (which returns a
**ratio**, not a percentage: 0.035).

## Reading MASE

| MASE | Meaning |
|---|---|
| 0.5 | Half the error of one-step seasonal naive |
| 1.0 | The same as it |
| 2.0 | Twice as much |

The denominator is a **one-step** error. The MASE of a multi-step forecast can
come out above 1 without that meaning it is bad: a distant horizon is simply
harder. Compare two methods at the same horizon with each other.

## The weighted percentage error

When summarising many series (hundreds of products) in one number, the measure
often used in place of MAPE:

$$\text{WAPE} = \frac{\sum \lvert e_t \rvert}{\sum \lvert y_t \rvert} \times 100$$

The total absolute error over the total actual value. Days with zero do not
break the denominator, and high-volume days get more weight. It is the
standard in retail.

## What a report should contain

1. The measure and its unit.
2. The horizon.
3. How many experiments, over which period.
4. The mean **and** the spread (the standard deviation, or best / worst).
5. The result of the baseline on the same rig.
6. The bias.

"MAE 17.2 (13 experiments, a 28-day horizon, 2024; worst 39.8); seasonal naive
17.9; bias +1.7" is a complete sentence. "The error is 12" is not.
