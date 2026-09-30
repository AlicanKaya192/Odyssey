## Which question, which chart

| Question | Chart | Preparing the data |
|---|---|---|
| What is the overall shape? | Line | `ax.plot(s.index, s)` |
| Is there a trend? | Raw + moving average | `s.rolling(n).mean()` |
| Is the pattern the same every year? | Seasonal plot | `groupby([index.month, index.year]).mean().unstack()` |
| What does the pattern look like? | Profile (bars) | `groupby(index.dayofweek).mean()` |
| What is the spread of the pattern? | Box plot | A separate list per day / month |
| Two patterns together? | Heatmap | `groupby([a, b]).mean().unstack()` |
| Does the series remember itself? | Lag plot | `ax.scatter(s.shift(k), s)` |
| How are several series doing? | Small multiples | `plt.subplots(n, 1, sharex=True)` |
| Which one grows faster? | An index (based at 100) | `wide / wide.iloc[0] * 100` |
| Who is ahead within the year? | Cumulative line | `s.groupby(index.year).cumsum()` |
| How are the changes distributed? | Histogram | `ax.hist(s.pct_change().dropna(), bins=50)` |
| What happened when? | Line + markers | `axvline`, `axvspan`, `annotate` |

## The date axis

```python
import matplotlib.dates as mdates

ax.xaxis.set_major_locator(mdates.YearLocator())             # every year
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))  # every three months
ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=0))   # every Monday
ax.xaxis.set_major_locator(mdates.HourLocator(interval=6))   # every six hours

ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))  # Jan 2024
ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))  # 09 Mar
ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))  # 14:30

fig.autofmt_xdate()                  # tilts the labels to fit
ax.set_xlim(pd.Timestamp("2024-03-01"), pd.Timestamp("2024-03-31"))
```

A shortcut: `mdates.ConciseDateFormatter(ax.xaxis.get_major_locator())`
shortens the labels by itself (the year is written only when it changes).

## Small multiples

Instead of putting several series on one axis, stack panels:

```python
fig, axes = plt.subplots(4, 1, figsize=(10, 8), sharex=True)
for ax, store in zip(axes, wide.columns):
    ax.plot(wide.index, wide[store])
    ax.set_ylabel(store)
```

`sharex=True` makes every panel show the same date range. `sharey=True` is
for comparing levels; if you are comparing patterns, let each panel keep its
own scale.

## Showing gaps honestly

```python
ax.plot(s.index, s)                      # the line breaks where there is NaN
ax.plot(s.index, s.interpolate(), linestyle=":")   # the filled part as a dotted line
```

A broken line is information: there is no data there. If you filled the gap,
show the filled part with a different line style.

If missing days are not there as rows at all, matplotlib joins the two
neighbouring points with a straight line and the gap does not show. Call
`asfreq` before plotting.

## Layers

```python
ax.plot(s.index, s, color="lightgray", linewidth=0.8)      # background
ax.plot(trend.index, trend, linewidth=2)                   # emphasis
ax.fill_between(s.index, low, high, alpha=0.2)             # a range / uncertainty
ax.axhline(s.mean(), linestyle="--")                       # a reference line
ax.axvspan(start, end, alpha=0.15)                         # a stretch of time
```

`fill_between` will be used a lot later: prediction intervals (Section 20)
are drawn this way.

## Saving

```python
fig.tight_layout()
fig.savefig("chart.png", dpi=110)
plt.close(fig)
```

`plt.show()` tries to open a window; in a script and in the exercises use
`savefig`. If you produce many charts in a loop, `plt.close(fig)` frees the
memory.

## The pandas shortcut

```python
ax = s.plot(figsize=(10, 4))                   # the date axis is ready
wide.plot(subplots=True, figsize=(10, 8))      # a panel per series
s.resample("ME").mean().plot(kind="bar")
```

Handy for a quick look. When fine tuning is needed you carry on with
matplotlib commands on the same `ax` object.
