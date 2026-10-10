## NumPy

| Code | What |
|---|---|
| `np.array(x, dtype="float32")` | an array, a type |
| `a.reshape(3, -1)`, `a.T` | shape, transpose |
| `a[a > 0]`, `a[[0, 2]]` | mask, index selection (copy) |
| `a[1:3]` | a slice (view) |
| `a.mean(axis=0)`, `keepdims=True` | column mean, keep the shape |
| `np.where(c, a, b)`, `np.select(...)` | conditions |
| `rng = np.random.default_rng(1)` | a generator |
| `np.linalg.solve(A, b)`, `lstsq` | equations, least squares |

## pandas

| Code | What |
|---|---|
| `df.set_index("a")`, `loc`, `iloc` | index, selection |
| `a.merge(b, on="k", how="left", validate="many_to_one")` | combine |
| `pd.concat(pieces, ignore_index=True)` | stack |
| `df.melt(...)`, `df.pivot_table(..., aggfunc="sum")` | shape |
| `pd.to_datetime(s, format=...)`, `s.dt.month` | dates |
| `s.resample("ME").sum()`, `rolling(7).mean()` | by time |
| `s.str.strip().str.lower()`, `str.extract(...)` | text |
| `s.astype("category")`, `pd.cut(...)` | categories |
| `df.loc[c, "a"] = 1` | change (one step) |
| `g.transform("sum")` | spread a group result to the rows |

## Charts

| Code | What |
|---|---|
| `fig, ax = plt.subplots(figsize=(6, 3), layout="constrained")` | a figure |
| `ax.plot`, `scatter`, `bar`, `hist`, `boxplot`, `imshow` | types |
| `ax.set(title=, xlabel=, ylabel=)` | text |
| `fig.savefig("a.png", dpi=200, bbox_inches="tight")`; `plt.close(fig)` | save, release |
| `sns.histplot(df, x=, hue=)`, `sns.barplot(..., estimator=)` | seaborn |
| `sns.relplot(..., col=)` | panels |

## SciPy

| Code | What |
|---|---|
| `stats.norm(m, s).sf(x)` | the probability above x |
| `stats.ttest_ind(a, b, equal_var=False)` | two groups |
| `res.confidence_interval()` | the difference's interval |
| `stats.chi2_contingency(table)` | categorical independence |
| `optimize.minimize(f, x0=...)` | minimise |
| `optimize.curve_fit(model, x, y, p0=...)` | fit a curve |
| `interpolate.PchipInterpolator(x, y)` | non-overshooting in-between values |

## Ten rules

1. Alignment is by label; `.values` drops the labels.
2. Use `how="left"` when adding information, then check the row count.
3. Read date text with `format=`; look at the `NaT` count.
4. Column operations instead of loops.
5. To change: `df.loc[condition, column] = value`.
6. The question first, then the chart; bars from zero.
7. Know which calculation seaborn does.
8. "Not significant" ≠ "no difference"; look at the confidence interval.
9. scipy minimises; for a maximum, the negative.
10. If there is randomness, write the seed.
