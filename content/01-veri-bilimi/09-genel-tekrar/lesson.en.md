# Overall Review

You are not learning anything new in this section. You are seeing how what
you have learned fits together.

Nine sections ago you were asking "what is data science". Now, when a raw
table lands in front of you, you can clean it, ask your questions of it, put
the answer into a chart and — most importantly — know not to say what the
data **does not** say.

## How the pieces connect

<figure class="fig">
  <div class="flow">
    <span class="node"><b>NumPy</b><br>vectorised maths</span>
    <span class="arrow">→</span>
    <span class="node"><b>Series</b><br>labelled data</span>
    <span class="arrow">→</span>
    <span class="node"><b>DataFrame</b><br>a table</span>
    <span class="arrow">→</span>
    <span class="node"><b>Selection</b><br>the part you care about</span>
    <span class="arrow">→</span>
    <span class="node ok"><b>Groups</b><br>comparison</span>
  </div>
  <figcaption>Each step is built on the one before. A DataFrame is nothing but Series placed side by side; a Series is a NumPy array with labels next to it.</figcaption>
</figure>

Cleaning, visualisation and exploration are the work that sits on top of that
chain: cleaning before you enter it, charts and exploration after you leave
it.

## An analysis from start to finish

Let us see what a real job looks like in a single example. We have a raw
table:

```python
import pandas as pd

raw = pd.DataFrame({
    "Name ": [" Ada", "Kerem", "Mina ", "Deniz", "Kerem"],
    "City": ["ankara", "Izmir ", "ANKARA", "Bursa", "Izmir "],
    "score": ["82", "74", "91", None, "74"],
    "hours": [10, 6, 12, 3, 6],
})
```

This table carries four separate diseases. You have seen all of them in the
previous sections.

### 1. Look first

```python
print(raw.shape)
print(raw.dtypes.astype(str).tolist())
```

```text
(5, 4)
['str', 'str', 'str', 'int64']
```

The `score` column is `str`. So you cannot take an average — a problem on the
very first step.

### 2. Column names

```python
data = raw.copy()
data.columns = data.columns.str.strip().str.lower()
print(data.columns.tolist())
```

```text
['name', 'city', 'score', 'hours']
```

`data["name"]` was not working because of the trailing space in `"Name "`.
The first thing cleaned is always the column names.

The `copy()` is deliberate too: keeping the raw data means you can go back
when you spot a mistake three steps later.

### 3. Text and types

```python
data["name"] = data["name"].str.strip()
data["city"] = data["city"].str.strip().str.title()
data["score"] = pd.to_numeric(data["score"], errors="coerce")

print(data)
```

```text
    name    city  score  hours
0    Ada  Ankara   82.0     10
1  Kerem   Izmir   74.0      6
2   Mina  Ankara   91.0     12
3  Deniz   Bursa    NaN      3
4  Kerem   Izmir   74.0      6
```

`"ankara"`, `"Izmir "` and `"ANKARA"` would have been three separate groups;
now they are two. `to_numeric` made `score` numeric and turned the `None`
into a proper `NaN`.

### 4. Duplicates and gaps

```python
data = data.drop_duplicates()
print(len(data))
print(data.isna().sum().tolist())

data = data.dropna(subset=["score"])
print(len(data))
```

```text
4
[0, 0, 1, 0]
3
```

Kerem had been entered twice and one copy is gone. Deniz, whose `score` was
blank, has dropped out of the analysis.

**That is a decision**, not a silent step: Deniz's record was removed and
that belongs in the report. Five records became three.

### 5. Ask

```python
print(data.groupby("city")["score"].agg(["count", "mean"]))
print(round(data["hours"].corr(data["score"]), 2))
```

```text
        count  mean
city
Ankara      2  86.5
Izmir       1  74.0
0.98
```

Ankara looks ahead. But look at the `count` column: 2 and 1.

**No conclusion about the cities comes out of this data.** The correlation of
0.98 was computed from three records too — a line through three points
always fits well.

The honest result of the analysis is this: *the data was cleaned, three
usable records remained, and no conclusion can be drawn from that many.*
That is not a failure, it is the finding itself.

## What you learned, section by section

| Section | The key idea |
|---|---|
| What Data Science Is | Data science starts with a question, not with data |
| NumPy | Vectorised operations instead of loops; an array holds one type |
| Series | **Labels** join the values; operations align on the labels |
| DataFrame | Series side by side; the columns can be of different types |
| Selecting and Filtering | `loc` by label, `iloc` by position; conditions with `&` and <code>&#124;</code> |
| Grouping | Split, compute, combine — several summaries with `agg` |
| Cleaning Data | Names → text → types → duplicates → gaps |
| Visualisation | One chart says one thing; the axis starts at zero |
| Exploratory Analysis | Question → look → finding → new question |

## The most common traps

The mistakes you met again and again in this module, in one list:

| Trap | The right way |
|---|---|
| Taking `mean()` with missing values | Checking how many with `isna().sum()` first |
| Reading a group average without `count` | `agg(["count", "mean"])` |
| Mistaking correlation for causation | Saying "they move together" |
| Chained assignment (`data[...][...] = ...`) | Writing in one step with `loc` |
| A bar chart axis not starting at zero | `ax.set_ylim(0, ...)` |
| Deleting an outlier without thinking | Asking "an error or genuine" first |
| Losing the result by expecting `inplace=True` | Storing the result in a variable |
| Overwriting the raw data | `copy()` and a separate output file |

## The next step

This module taught you **how to work with a dataset**. Prediction comes
next: looking at past data to say something about the future — machine
learning.

But it is worth knowing one thing before you go there: **most of the time in
a machine learning project goes on the work you learned in this module.**
Fitting a model is a few lines; understanding the data, cleaning it and
finding the right question takes weeks.

That is why every section here carries over.

## Summary

- The **NumPy → Series → DataFrame** chain: each layer sits on the one
  before.
- A real analysis: look → clean → ask → show → turn into a sentence.
- **Cleaning is a series of decisions**, not a mechanical step; what you did
  goes in the report.
- **The raw data is preserved** and you work on a copy.
- A group average is not read without `count`, a correlation not as
  causation, a chart not without a title.
- The honest result of an analysis is sometimes **"this question cannot be
  answered with this data"**. Being able to say that beats making something
  up.
