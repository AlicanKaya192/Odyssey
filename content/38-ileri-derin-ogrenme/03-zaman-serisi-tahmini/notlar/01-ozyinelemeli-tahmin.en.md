The lesson's model always forecast **one day** ahead and saw the real values
every day. If two weeks ahead is wanted, the real values do not exist yet:
the model's own forecast has to be appended to the end of the window to
forecast the next day (a recursive forecast). The code below uses the
lesson's model and variables; every 7 days in the test period it forecasts 14
days from a new start point and compares them with the one-day forecasts of
the same days.

```python
def recursive(start, days=14):
    window = torch.tensor(scaled[start - 28:start]).reshape(1, 28, 1)
    preds = []
    with torch.no_grad():
        for _ in range(days):
            p = model(window)
            preds.append(p.item())
            window = torch.cat([window[:, 1:], p.reshape(1, 1, 1)], dim=1)
    return np.array(preds) * std + mean


starts = range(split, len(series) - 14, 7)
errors_multi, errors_one = [], []
for s in starts:
    days = series[s:s + 14]
    errors_multi.append(np.abs(recursive(s) - days).mean())
    errors_one.append(np.abs(pred[s - split:s - split + 14] - days).mean())
print(len(starts), np.mean(errors_multi) > np.mean(errors_one))
```

```text
13 True
```

- `torch.cat([window[:, 1:], ...], dim=1)`: drops the oldest day of the
  window and appends the forecast to the end; the window always stays 28
  days.
- On average over the 13 start points the recursive forecast's error is
  larger than the one-day forecast's: each forecast's error becomes the
  **input** of the next forecast and errors pile up.
- Looking one by one, a few windows show the opposite. Deciding from a single
  14-day window is therefore misleading; as in the Time Series track, look at
  the average over several cuts.

## Three roads to several days ahead

| Road | How | Pros / cons |
|---|---|---|
| Recursive | Feed the one-step model's forecast back in | One model; errors pile up |
| Direct | A separate model per horizon (1 day, 2 days, ...) | No piling up; many models |
| Multi-output | Last layer `nn.Linear(hidden, 14)`: give all 14 days at once | One model, no piling up; the most common deep learning road |
