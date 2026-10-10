## Plotting methods

| Code | Draws |
|---|---|
| `ax.plot(x, y, marker="o")` | a line |
| `ax.scatter(x, y, c=z, s=20, cmap="viridis", alpha=0.5)` | a scatter |
| `ax.bar(names, values)` / `ax.barh(...)` | vertical / horizontal bars |
| `ax.bar(x, b, bottom=a)` | stacked bars |
| `ax.bar(x - w/2, a, width=w)` + `ax.bar(x + w/2, b, width=w)` | grouped bars |
| `ax.hist(v, bins=20, range=(0, 80), density=True)` | a histogram |
| `ax.boxplot([a, b], tick_labels=["A", "B"])` | a box plot |
| `ax.violinplot([a, b])` | a violin (the shape of the distribution) |
| `ax.imshow(m, cmap="RdBu_r", vmin=-1, vmax=1)` | a heat map |
| `ax.fill_between(x, low, high, alpha=0.3)` | a band |
| `ax.errorbar(x, y, yerr=e, fmt="o")` | error bars |
| `ax.pie(shares, labels=names)` | a pie (only 2–3 parts) |

## Helpers

| Code | What it does |
|---|---|
| `fig.colorbar(obj, ax=ax, label="...")` | the colour scale's legend |
| `ax.set_xticks(positions, labels)` | tick positions and text |
| `ax.text(x, y, "text", ha="center")` | text in a cell |
| `ax.legend()` | a legend for those given `label=` |

## Choosing a colour scale

| Data | Scale |
|---|---|
| One-sided (from 0 upward) | `viridis`, `Blues` |
| Two-sided (−…+) | `RdBu_r`, `coolwarm` + symmetric `vmin`/`vmax` |
| Categories | `tab10` (the default cycle) |

## Errors

| Symptom | Cause |
|---|---|
| Two histograms cannot be compared | different `bins` / `range` |
| Stacked bars overlap | no `bottom=` given |
| Grouped bars in one place | `x` not shifted (`x ± w/2`) |
| Zero looks coloured in a heat map | `vmin`/`vmax` not symmetric |
| No density visible in a scatter | too many points; `alpha` |
| `boxplot() got an unexpected keyword argument` | old code `labels=`; the new one is `tick_labels=` |
