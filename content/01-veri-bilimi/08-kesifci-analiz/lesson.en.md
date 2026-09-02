# Exploratory Data Analysis

So far you have learned tools one at a time: selecting, filtering, grouping,
cleaning, plotting. **Exploratory data analysis** (EDA) is what tells you in
which order to use them, and why.

In one sentence: knowing what to do when a new dataset lands in front of you.

## It is not a step, it is a loop

Beginners take EDA for "the preparation you do before the analysis". It is
not.

<figure class="fig">
  <div class="flow">
    <span class="node acc"><b>Question</b><br>what am I curious about</span>
    <span class="arrow">→</span>
    <span class="node"><b>Look</b><br>table, number, chart</span>
    <span class="arrow">→</span>
    <span class="node"><b>Finding</b><br>what I saw</span>
    <span class="arrow">→</span>
    <span class="node"><b>New question</b></span>
  </div>
  <figcaption>Every finding raises a new question. The loop stops not when the questions run out, but when the answers start telling a story.</figcaption>
</figure>

"The average score is 71" is a finding. But the next thing follows straight
away: whose scores are low? Why? Did they study less, or is something else
going on?

In this section you will walk through a dataset with that eye.

## The data

```python
import pandas as pd

data = pd.DataFrame({
    "city": ["Ankara", "Izmir", "Ankara", "Bursa", "Izmir", "Ankara", "Bursa", "Izmir"],
    "age": [24, 31, 28, 45, 22, 38, 52, 27],
    "hours": [12, 5, 9, 2, 14, 7, 3, 11],
    "score": [88, 62, 82, 45, 91, 70, 51, 84],
})
```

Eight people: city, age, study hours and exam score.

In reality the row count may be hundreds of thousands, but **the order you
look in does not change.**

## Step 1: shape and types

```python
print(data.shape)
print(data.dtypes.astype(str).tolist())
```

```text
(8, 4)
['str', 'int64', 'int64', 'int64']
```

The first question is "how many rows, how many columns". The second is "is
every column the type I expect".

If a numeric column shows up as `str` the data has not been cleaned — the
subject of the previous section. You need to see that before you start the
analysis, not while taking an average.

## Step 2: look with your eyes

```python
print(data.head(3))
```

```text
     city  age  hours  score
0  Ankara   24     12     88
1   Izmir   31      5     62
2  Ankara   28      9     82
```

This step gets skipped, and it is the cheapest one. Three rows answer "what
is in this column" without any statistics at all.

## Step 3: are there missing values

```python
print(data.isna().sum().tolist())
```

```text
[0, 0, 0, 0]
```

There are none here. If there were, two questions would follow: **how many**
and **why**.

The second is the one that matters. If the income column of a survey is
empty, those people may not be randomly distributed — usually it is the
high earners who do not answer. Dropping the missing rows then skews the
data systematically.

## Step 4: describe

```python
print(data.describe())
```

```text
             age     hours      score
count   8.000000   8.00000   8.000000
mean   33.375000   7.87500  71.625000
std    10.662853   4.35685  17.459647
min    22.000000   2.00000  45.000000
25%    26.250000   4.50000  59.250000
50%    29.500000   8.00000  76.000000
75%    39.750000  11.25000  85.000000
max    52.000000  14.00000  91.000000
```

Learning to **read** this table is half of EDA. You look at three things:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">mean ↔ 50%</span><span class="anat-body">if the mean and the median are far apart the distribution is skewed; there are extremes</span></div>
    <div class="anat-row"><span class="anat-label">std</span><span class="anat-body">the spread — small means everyone is alike, large may mean two different groups</span></div>
    <div class="anat-row"><span class="anat-label">min / max</span><span class="anat-body">do they make sense? an age of 0 or 200 means a data error</span></div>
  </div>
</figure>

Here `score` has a mean of 71.6 and a median of 76. **The mean is below the
median**, so a few low scores at the bottom are dragging it down.

Noticing that raises a new question: who are those low scorers?

## Step 5: categorical columns

```python
print(data["city"].value_counts())
```

```text
city
Ankara    3
Izmir     3
Bursa     2
Name: count, dtype: int64
```

This is the first thing you ask of a categorical column. You see two things
at once: how many distinct values there are, and whether they are
**balanced**.

The imbalance matters: if a group has 2 people in it, there is very little
you can say about that group's average.

## Step 6: compare the groups

Let us start the search for the low scorers with the city:

```python
print(data.groupby("city")["score"].agg(["count", "mean"]))
```

```text
        count  mean
city
Ankara      3  80.0
Bursa       2  48.0
Izmir       3  79.0
```

Bursa is 48, the others 79-80. A big gap.

**But look at the `count` column: Bursa has two people.** Going from two
people to "scores are low in Bursa" is mistaking two people for a city.

That is why you ask for `count` alongside `mean`. Had you seen the average
alone, you would have walked into the trap.

<figure class="fig">
  <div class="versus">
    <div class="versus-side">
      <h4>Finding</h4>
      <p>In this data the two people from Bursa scored low.</p>
    </div>
    <div class="versus-side">
      <h4>Claim</h4>
      <p>Scores are low in Bursa.</p>
    </div>
  </div>
  <figcaption>The first is read off the data; the second is something the data does not say. Keeping the difference is exactly what honesty in analysis means.</figcaption>
</figure>

## Step 7: relationships between numeric columns

```python
print(round(data["hours"].corr(data["score"]), 2))
```

```text
0.98
```

**Correlation** tells you whether two numeric columns move together, as a
number between -1 and +1:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">near +1</span><span class="anat-body">as one rises the other rises too</span></div>
    <div class="anat-row"><span class="anat-label">around 0</span><span class="anat-body">no linear relationship is visible</span></div>
    <div class="anat-row"><span class="anat-label">near -1</span><span class="anat-body">as one rises the other falls</span></div>
  </div>
</figure>

0.98 is very high. Study hours and score move together.

You can also compare all the numeric columns at once:

```python
print(data[["age", "hours", "score"]].corr().round(2))
```

```text
        age  hours  score
age    1.00  -0.89  -0.91
hours -0.89   1.00   0.98
score -0.91   0.98   1.00
```

The diagonal is always 1.00 — every column agrees perfectly with itself. The
upper and lower triangles are the same; reading it once is enough.

Here `age` and `score` show -0.91: as age rises the score falls. But `age`
and `hours` are -0.89 too. That is, the older people **studied less**. Is it
age or study hours that lowers the score? This data cannot say.

**Correlation is not causation.** When three columns are tangled together,
separating out which one is the cause is a separate job.

## Step 8: outliers

Rather than hunting for outliers by eye, you use a rule. The most common is
the **IQR rule**:

```python
values = pd.Series([12, 15, 14, 13, 16, 15, 92])

q1 = values.quantile(0.25)
q3 = values.quantile(0.75)
iqr = q3 - q1

low = q1 - 1.5 * iqr
high = q3 + 1.5 * iqr

print(q1, q3, iqr)
print(low, high)
print(values[(values < low) | (values > high)].tolist())
```

```text
13.5 15.5 2.0
10.5 18.5
[92]
```

`quantile(0.25)` is the value a quarter of the data falls below, and
`quantile(0.75)` three quarters. The distance between them is the
**interquartile range** (IQR), and it shows how widely the middle half of
the data is spread.

Values more than 1.5 times that range outside the interval count as
outliers. `92` was caught.

You can see why it matters in the mean:

```python
print(values.mean())
print(values.median())
```

```text
25.285714285714285
15.0
```

A single value pushed the mean from 15 to 25. **The median did not budge.**
When you suspect an outlier, the median is the more reliable summary.

## Turning a finding into a sentence

What comes out at the end of an analysis is not a table but **a sentence**. A
good finding says three things: what you saw, how strong it is, and what you
are not saying.

> In this eight-person dataset there is a strong relationship between study
> hours and score (correlation 0.98). The Bursa average looks low, but there
> are only two records there, so no conclusion can be drawn about the city.

Compare:

> Studying raises the score. Education quality is poor in Bursa.

The second looks as though it came from the same data, but it carries two
extra claims: causation, and a generalisation from a group of two to a
whole city.

## The order

<figure class="fig">
  <div class="flow">
    <span class="node acc"><b>1</b><br>shape, dtypes</span>
    <span class="arrow">→</span>
    <span class="node"><b>2</b><br>head</span>
    <span class="arrow">→</span>
    <span class="node"><b>3</b><br>isna</span>
    <span class="arrow">→</span>
    <span class="node"><b>4</b><br>describe</span>
    <span class="arrow">→</span>
    <span class="node"><b>5</b><br>value_counts</span>
    <span class="arrow">→</span>
    <span class="node"><b>6</b><br>groupby</span>
    <span class="arrow">→</span>
    <span class="node"><b>7</b><br>corr</span>
  </div>
  <figcaption>Not an order to memorise, but knowing where to start when you open a new dataset saves you time.</figcaption>
</figure>

What comes out of each step steers the next. If the mean and the median are
far apart in `describe` you go and look for outliers; if `value_counts` shows
an unbalanced group you tread carefully when grouping.

## Summary

- **EDA is a loop:** question → look → finding → new question.
- The order: `shape`/`dtypes` → `head` → `isna` → `describe` →
  `value_counts` → `groupby` → `corr`.
- **`describe` is read:** the gap between mean and median shows skew, `std`
  the spread, `min`/`max` a data error.
- **A group average is not read without `count`.** A group of two is not a
  conclusion.
- **Correlation** measures movement together, not the cause. A third column
  may explain both.
- **The IQR rule** finds outliers by rule: outside 1.5 times the
  interquartile range.
- When there is an outlier, **the median is more reliable than the mean**.
- A finding also says what it is **not** saying.
