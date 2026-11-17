In the lesson we took the scaling mean from the first 630 days only. Let us
see in numbers why this matters on a series with a trend.

```python
import numpy as np
from dl_data import make_series

series = make_series(730)
split = 630
print(round(float(series[:split].mean())))
print(round(float(series.mean())))
print(round(float(series[split:].mean())))
```

```text
58
57
54
```

- The training period's mean is 58, the whole series'
  57, the test period's 54: the yearly season pulls
  the series down in the test period. Scaled with the whole series, the
  model would indirectly "know" the level of the test period during
  training.
- In real use the future is not at hand; measurement must work the same
  way. The rule is the same as for table data: **every statistic from
  training only**.

## Dealing with a trend

Because the scaled series keeps rising, the test period can climb to values
training never saw. Networks forecast badly outside the range they have
seen. Two common remedies:

| Remedy | How | Turning back |
|---|---|---|
| Differencing | Target `y[t] - y[t-1]`: forecast the change | Add the forecast to the last real value |
| Scale per window | Centre each window on its own mean | Add that mean back to the forecast |

Both are the deep learning counterpart of the stationarity idea in the Time
Series track: teach the model the pattern, not the level.
