```python
import matplotlib
matplotlib.use("Agg")     # needed inside Odyssey; not on your own machine
import matplotlib.pyplot as plt
```

## Canvas and axes

| Written as | What it does |
|---|---|
| `fig, ax = plt.subplots()` | A canvas with one drawing area |
| `plt.subplots(1, 2)` | Two areas side by side |
| `plt.subplots(2, 1)` | Two areas stacked |
| `plt.subplots(figsize=(10, 4))` | Canvas size (in inches) |
| `fig.axes` | All the drawing areas on the canvas |
| `plt.close(fig)` | Closes the canvas (for memory) |

In loops that draw many charts you need `plt.close(fig)`, or open canvases
pile up.

## Chart types

| Written as | What it draws |
|---|---|
| `ax.bar(x, y)` | Vertical bars |
| `ax.barh(x, y)` | Horizontal bars — for long category names |
| `ax.plot(x, y)` | A line |
| `ax.plot(x, y, marker="o")` | A line with points |
| `ax.scatter(x, y)` | A scatter plot |
| `ax.hist(values, bins=10)` | A histogram |
| `ax.pie(values, labels=names)` | A pie — unreadable beyond three slices |
| `ax.boxplot(values)` | A box plot — median, quartiles, outliers |

## Labelling

| Written as | What it does |
|---|---|
| `ax.set_title("...")` | The title |
| `ax.set_xlabel("...")` / `ax.set_ylabel("...")` | Axis labels |
| `ax.legend()` | A legend box (when there are several series) |
| `ax.set_xlim(0, 100)` / `ax.set_ylim(0, 100)` | The axis range |
| `ax.set_xticks([...])` | Which values are marked |
| `ax.tick_params(axis="x", rotation=45)` | Rotate the labels |
| `ax.grid(True, alpha=0.3)` | Grid lines |

A title and axis labels are **required**. So are units: not "Sales" but
"Sales (thousands)".

## Reading information back

| Written as | What it gives |
|---|---|
| `ax.get_title()` | The title text |
| `ax.get_xlabel()` / `ax.get_ylabel()` | The axis labels |
| `ax.patches` | The bars (countable with `len`) |
| `ax.lines` | The lines |
| `ax.get_ylim()` | The axis range |
| `p.get_height()` | The height of a bar |

These are useful when writing tests and confirming a chart was drawn
correctly.

## Several series

```python
fig, ax = plt.subplots()
ax.plot(months, ankara, marker="o", label="Ankara")
ax.plot(months, izmir, marker="s", label="Izmir")
ax.legend()
```

Calling `legend()` without giving `label`s produces an empty box.

## Colour and style

| Written as | What it does |
|---|---|
| `ax.bar(x, y, color="steelblue")` | A single colour |
| `ax.bar(x, y, color=["red", "gray", "gray"])` | A colour per bar |
| `ax.plot(x, y, linestyle="--")` | A dashed line |
| `ax.plot(x, y, linewidth=2)` | Thickness |
| `ax.scatter(x, y, alpha=0.5)` | Transparency — for overlapping points |
| `ax.axhline(y=50, color="red")` | A horizontal reference line |

**One accent colour and grey for the rest** is the most readable choice for
most charts: the eye knows where to look.

## Saving

| Written as | What it does |
|---|---|
| `fig.savefig("chart.png")` | Saves it |
| `fig.savefig("chart.png", dpi=150)` | Resolution |
| `fig.savefig("chart.png", bbox_inches="tight")` | Trims the excess margin |
| `fig.savefig("chart.svg")` | Vector — does not blur when scaled |

For a report, `dpi=150` and `bbox_inches="tight"` are good defaults.

## The pandas shortcut

| Written as | What it draws |
|---|---|
| `data.plot(kind="bar", x="city", y="score")` | Bars |
| `data.plot(kind="line", x="month", y="sales")` | A line |
| `data["score"].plot(kind="hist", bins=10)` | A histogram |
| `data.plot(kind="scatter", x="hours", y="score")` | A scatter plot |
| `data["city"].value_counts().plot(kind="bar")` | A count chart |

Handy for a quick look. With the `ax=ax` argument you can also draw into your
own axes:

```python
fig, ax = plt.subplots()
data.plot(kind="bar", x="city", y="score", ax=ax)
ax.set_title("...")
```

## Common patterns

```python
# A group result as bars
averages = data.groupby("city")["score"].mean()

fig, ax = plt.subplots()
ax.bar(averages.index, averages.values)
ax.set_ylim(0, 100)
ax.set_title("Average score by city")

# A distribution with the mean marked
fig, ax = plt.subplots()
ax.hist(data["score"], bins=10)
ax.axvline(data["score"].mean(), color="red", linestyle="--")

# Two charts side by side
fig, (left, right) = plt.subplots(1, 2, figsize=(10, 4))
left.bar(...)
right.hist(...)
fig.tight_layout()
```

`fig.tight_layout()` stops the drawing areas overlapping; on multi-area
canvases you almost always need it.
