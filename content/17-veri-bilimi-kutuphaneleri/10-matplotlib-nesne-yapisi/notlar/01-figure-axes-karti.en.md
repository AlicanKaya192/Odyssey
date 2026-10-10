## Building

| Code | Gives |
|---|---|
| `fig, ax = plt.subplots()` | one figure, one area |
| `fig, axes = plt.subplots(2, 3)` | a `(2, 3)` array |
| `plt.subplots(1, 3)` | a one-dimensional array |
| `plt.subplots(..., squeeze=False)` | always two-dimensional |
| `plt.subplots(..., sharex=True, sharey=True)` | shared axes |
| `plt.subplots(..., figsize=(8, 4), dpi=100)` | inches and resolution |
| `plt.subplot_mosaic([["a", "b"]])` | named areas (a dictionary) |
| `layout="constrained"` | keep text from overlapping |

## Area (Axes)

| Code | What it does |
|---|---|
| `ax.set(title=, xlabel=, ylabel=)` | several settings |
| `ax.set_xlim(0, 10)` / `ax.get_xlim()` | axis limits |
| `ax.legend()` | a legend for lines given `label=` |
| `ax.lines`, `ax.patches` | drawn lines / bars |
| `ax.xaxis`, `ax.yaxis` | single axis objects |
| `ax.twinx()` | the same x, a second y axis |

## Figure

| Code | What it does |
|---|---|
| `fig.suptitle("...")` | the whole figure's title |
| `fig.savefig("a.png", dpi=200, bbox_inches="tight")` | save |
| `fig.get_size_inches()` | size (inches) |
| `fig.axes` | all areas |
| `plt.close(fig)` / `plt.close("all")` | release |

## pyplot ↔ objects

| pyplot | Object |
|---|---|
| `plt.plot(x, y)` | `ax.plot(x, y)` |
| `plt.title("t")` | `ax.set_title("t")` |
| `plt.xlabel("x")` | `ax.set_xlabel("x")` |
| `plt.xlim(0, 5)` | `ax.set_xlim(0, 5)` |
| `plt.gcf()` / `plt.gca()` | `fig` / `ax` |

## Errors

| Symptom | Cause |
|---|---|
| `'Axes' object has no attribute 'xlabel'` | on the object `set_xlabel`; `xlabel` is pyplot's |
| `'Text' object is not callable` | `ax.title(...)` was written; `ax.set_title(...)` |
| `'numpy.ndarray' object has no attribute 'plot'` | `axes` is an array; pick with `axes[0]` |
| `too many indices for array` | `plt.subplots(1, 3)` is one-dimensional |
| Two charts' heights mislead | no `sharey=True` |
| `More than 20 figures have been opened` | no `plt.close(fig)` in the loop |
| Labels overlap | `layout="constrained"` |
