Some tables share not the same key but **the nearest time**. A trade
happened at 09:00:07; the price table has no such second, but a price
updated at 09:00:05. The right match is "the last price before that moment".
`merge` needs exact equality and matches none of them; `merge_asof` is made
for this.

```python
import pandas as pd


def at(*times):
    return pd.to_datetime(list(times), format="%H:%M:%S")


trades = pd.DataFrame({"time": at("09:00:03", "09:00:07", "09:01:30"),
                       "qty": [5, 2, 8]})
quotes = pd.DataFrame({"time": at("09:00:00", "09:00:05", "09:01:00"),
                       "price": [10.0, 10.2, 10.1]})
both = pd.merge_asof(trades, quotes, on="time")
print(both["price"].tolist())
near = pd.merge_asof(trades, quotes, on="time", tolerance=pd.Timedelta("20s"))
print(near["price"].tolist())
fwd = pd.merge_asof(trades, quotes, on="time", direction="forward")
print(fwd["price"].tolist())
print(both.assign(time=both["time"].dt.strftime("%H:%M:%S")))
```

```text
[10.0, 10.2, 10.1]
[10.0, 10.2, nan]
[10.2, 10.1, nan]
       time  qty  price
0  09:00:03    5   10.0
1  09:00:07    2   10.2
2  09:01:30    8   10.1
```

## How does it work?

- For each row on the left it takes the last row on the right whose time is
  **less than or equal** to its own (`direction="backward"`, the default).
  The trade at 09:00:07 got the price 10.2 from 09:00:05.
- `tolerance=pd.Timedelta("20s")`: if the nearest price is older than 20
  seconds, do not match; leave `NaN`. The last price for the 09:01:30 trade
  was 30 seconds earlier, so it stayed empty. Important for not computing
  with stale data.
- `direction="forward"` takes the next value; `"nearest"` whichever is
  closer.

## Conditions

- Both tables must be **sorted** by the `on` column; otherwise pandas raises
  an error (`left keys must be sorted`). `sort_values("time")` first.
- If the time series of several objects are in the same table (many stocks),
  `by="symbol"` matches each object within itself.
- Matching a sensor reading to the nearest weather record, an order to the
  exchange rate of that moment, an event to the setting at that moment are
  all the same pattern.
