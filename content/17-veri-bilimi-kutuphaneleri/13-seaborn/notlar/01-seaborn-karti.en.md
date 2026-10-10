## Functions

| Question | Axes-level (`ax=`) | Figure-level (panels) |
|---|---|---|
| Distribution | `histplot`, `kdeplot`, `ecdfplot` | `displot` |
| Category | `boxplot`, `violinplot`, `barplot`, `countplot`, `stripplot` | `catplot` |
| Relationship | `scatterplot`, `lineplot` | `relplot` |
| Regression | `regplot` | `lmplot` |
| Table | `heatmap` | `clustermap` |
| All at once | — | `pairplot`, `jointplot` |

## Common parameters

| Code | What it does |
|---|---|
| `data=df, x="a", y="b"` | a DataFrame and column names |
| `hue="c"` | group by colour |
| `style="c"`, `size="c"` | by marker / by size |
| `col="c"`, `row="c"`, `col_wrap=3` | split into panels (figure-level) |
| `order=[...]`, `hue_order=[...]` | category order |
| `estimator="sum"`, `errorbar=None` | the barplot / lineplot calculation |
| `stat="density"`, `common_norm=False` | compare groups of different sizes |
| `height=2.5, aspect=1.2` | panel size (figure-level) |
| `palette="colorblind"` | colour palette |

## Look

| Code | What it does |
|---|---|
| `sns.set_theme(style="whitegrid")` | a general style (lasting) |
| `sns.set_context("talk")` | text and line size (for slides) |
| `sns.despine()` | remove the top and right frame |
| `grid.set_titles("{col_name}")` | panel titles |
| `grid.set_axis_labels("x", "y")` | panel axis names |
| `grid.figure.savefig("a.png")` | save a figure-level chart |

## Traps

| Symptom | Cause |
|---|---|
| Bar height smaller than the total | `barplot` draws the mean |
| A smooth line not in the data | `lineplot` averages equal x values |
| A small group does not show | raw counts; `stat="density"` |
| `is a figure-level function and does not accept the ax= parameter` | figure-level takes no `ax`; it warns and opens a new figure |
| `load_dataset` hangs | it needs the internet |
| Categories in alphabetical order | give `order=` |
