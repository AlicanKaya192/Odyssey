The question "which form is right?" has a name: **tidy data**. It has three
rules:

1. Each **variable** is a column (city, year, score).
2. Each **observation** is a row (one student's score in one year).
3. Each cell holds **one** value.

A wide table breaks the first rule: `score_2024` and `score_2025` are two
separate columns but really one variable (score) at two values of another
variable (year). The year is hidden **inside the column name**.

```python
import pandas as pd

wide = pd.DataFrame({"id": [1, 2], "score_2024": [60, 75], "score_2025": [70, 80]})
long = pd.wide_to_long(wide, stubnames="score", i="id", j="year", sep="_")
print(long.reset_index().values.tolist())
```

```text
[[1, 2024, 60], [2, 2024, 75], [1, 2025, 70], [2, 2025, 80]]
```

- `wide_to_long` is written for this pattern: `stubnames="score"` is the
  common start of the column names, `sep="_"` the separator, and the rest of
  the name (`2024`) goes to the `j="year"` column and **is turned into a
  number**.
- `melt` could do it too, but then the year would have to be cut out of the
  text `"score_2024"` and converted separately.

## Why bother?

- `groupby("year")`, `df[df["year"] == 2025]`, `hue="year"` in a chart: each
  is one line when year is a **column**. In a wide table every new year means
  a new column name in the code.
- The third rule (one value) is what `explode` is about: `"gift,fast"` is two
  values in one cell; counting is impossible without opening it.

## Reports wide, analysis long

Tidy data is for **analysis**. The final table shown to a person is usually
wide (months side by side). The flow: bring the data to the long form →
compute → widen with `pivot_table` to show the result.
