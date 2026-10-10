## Axes

| Code | What it does |
|---|---|
| `ax.yaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))` | thousands separators |
| `ax.yaxis.set_major_formatter(PercentFormatter(xmax=1))` | 0.18 → 18% |
| `ax.set_yscale("log")` | a log axis |
| `ax.set_xlim(0, 10)` / `ax.invert_yaxis()` | limits / flip |
| `ax.tick_params(axis="x", rotation=45)` | rotate tick labels |
| `ax.xaxis.set_major_locator(mdates.MonthLocator())` | one tick per month |
| `ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))` | date format |
| `ax2 = ax.twinx()` | a second y axis on the right |

## Notes and emphasis

| Code | What it does |
|---|---|
| `ax.annotate("t", xy=(x, y), xytext=(x2, y2), arrowprops=dict(arrowstyle="->"))` | a note with an arrow |
| `ax.axhline(y)` / `ax.axvline(x)` | a reference line |
| `ax.axvspan(x1, x2, alpha=0.2)` | shade a range |
| `ax.bar_label(bars, padding=3)` | write values on bars |
| `bars[i].set_color("tab:blue")` | highlight one bar |
| `ax.spines[["top", "right"]].set_visible(False)` | remove the frame |
| `ax.legend(loc="upper left", frameon=False)` | legend position |

## Global settings

| Code | Scope |
|---|---|
| `with plt.rc_context({...}):` | only the block |
| `plt.rcParams["font.size"] = 11` | the rest of the script |
| `plt.style.use("tableau-colorblind10")` | the rest of the script |
| `with plt.style.context("ggplot"):` | only the block |

## Checklist

- Does the title say the message ("A sells 20% more than B")?
- Do the axis names carry units?
- Are numbers readable (`1,250,000`, not `1e6`)?
- Is there a single highlight colour?
- Does it read without colour too (markers, labels)?
- Does a bar axis start at zero; is a log axis announced?
