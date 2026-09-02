# Pandas Series

There was one thing a NumPy array did not know: **the names of its
elements.** Your scores sat there as `[82, 74, 91]`, but which one belonged
to whom was not something the array held.

pandas's answer is the **Series**: a NumPy array with **labels** travelling
alongside it.

```python
import pandas as pd
```

`pd` is a convention, just like `np`.

## Your first Series

```python
scores = pd.Series([82, 74, 91, 68])
print(scores)
```

```text
0    82
1    74
2    91
3    68
dtype: int64
```

The left column is the **index**, the right one the **values**. If you do not
give an index, pandas numbers them from 0.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">index</span><span class="anat-body">the labels — can be numbers, text or dates</span></div>
    <div class="anat-row"><span class="anat-label">values</span><span class="anat-body">the actual data; a NumPy array underneath</span></div>
    <div class="anat-row"><span class="anat-label">dtype</span><span class="anat-body">the shared type of the values — the rule inherited from NumPy</span></div>
    <div class="anat-row"><span class="anat-label">name</span><span class="anat-body">the Series' name; it becomes the column name inside a table</span></div>
  </div>
</figure>

## A labelled index

This is where the real power is:

```python
scores = pd.Series([82, 74, 91], index=["Ada", "Kerem", "Mina"])
print(scores)
print(scores["Mina"])
```

```text
Ada      82
Kerem    74
Mina     91
dtype: int64
91
```

You no longer have to say "the third element"; you call it by name. In NumPy
you would have kept a separate array of names and matched up the indices
yourself.

It can also be built from a dictionary — the keys become the index:

```python
population = pd.Series({"Ankara": 5, "Izmir": 4})
print(population)
```

```text
Ankara    5
Izmir     4
dtype: int64
```

## What comes from NumPy

Because a Series sits on top of a NumPy array, vectorised operations work
exactly the same:

```python
scores = pd.Series([82, 74, 91], index=["Ada", "Kerem", "Mina"])

print(scores + 5)
print(scores.mean())
print(scores[scores > 80])
```

```text
Ada      87
Kerem    79
Mina     96
dtype: int64
82.33333333333333
Ada     82
Mina    91
dtype: int64
```

Notice: selecting by condition **brings the labels along.** The result is not
just the numbers but who scored what.

## Alignment: the real trick

When you add two Series, pandas looks at the **labels, not the order**:

```python
a = pd.Series([1, 2, 3], index=["x", "y", "z"])
b = pd.Series([10, 20, 30], index=["z", "y", "x"])

print(a + b)
```

```text
x    31
y    22
z    13
dtype: int64
```

`b` is in reverse order, but the result is right: `x` was added to `x`, `y`
to `y`. NumPy would have added them in order without looking at the labels
and given a **silently wrong** answer.

This is called **alignment** and it is pandas's most valuable feature. When
you combine data from two different sources you do not have to hope the rows
line up.

If a label exists on only one side the result is `NaN`:

```python
a = pd.Series([1, 2], index=["x", "y"])
b = pd.Series([10, 20], index=["y", "z"])

print(a + b)
```

```text
x     NaN
y    12.0
z     NaN
dtype: float64
```

This is not an error but information: `x` exists only on one side and `z`
only on the other. Rather than making something up, pandas says "unknown".

## Missing values: different from NumPy

This part needs care.

```python
values = pd.Series([80.0, None, 90.0])

print(values.mean())
```

```text
85.0
```

The same data gave `nan` in NumPy. **pandas skips missing values in
calculations by itself.**

<figure class="fig">
  <div class="versus">
    <div class="versus-side">
      <h4>NumPy</h4>
      <p><code>mean()</code> gives <code>nan</code>. To skip you have to say <code>nanmean</code>.</p>
    </div>
    <div class="versus-side">
      <h4>pandas</h4>
      <p><code>mean()</code> skips the missing ones. If you want them counted you say so separately.</p>
    </div>
  </div>
  <figcaption>Two libraries answer the same question differently. You need to know which one you are working with — this difference can produce a silently wrong result.</figcaption>
</figure>

It looks like a convenience, but it carries a risk: **you may not notice how
many values were missing.** The average was computed, a number came back —
but perhaps eighty of your hundred records were empty.

So you count before you average:

```python
values = pd.Series([80.0, None, 90.0])

print(values.isna().sum())
print(values.count())
print(values.size)
```

```text
1
2
3
```

`count()` counts the **filled** cells, `size` counts all of them. If the two
differ, there are missing values.

## Filling and dropping

```python
values = pd.Series([80.0, None, 90.0])

print(values.fillna(0).tolist())
print(values.dropna().tolist())
print(values.fillna(values.mean()).tolist())
```

```text
[80.0, 0.0, 90.0]
[80.0, 90.0]
[80.0, 85.0, 90.0]
```

All three return a **new Series**; the original is untouched. Almost every
method in pandas works this way.

Which one you choose depends on the data: filling with zero says "the
measurement was zero" and drags the average down. Filling with the mean does
not preserve information but does not distort the average. Dropping loses the
record entirely.

## Counting in categorical columns

On a Series holding text, the thing you need most is "how many of each":

```python
cities = pd.Series(["Ankara", "Izmir", "Ankara", "Bursa", "Ankara"])

print(cities.value_counts())
print(cities.nunique())
```

```text
Ankara    3
Izmir     1
Bursa     1
Name: count, dtype: int64
3
```

`value_counts()` sorts from most to least. When you first open a dataset,
making this call on the categorical columns becomes almost a reflex.

## A quick look

```python
scores = pd.Series([82, 74, 91, 68])
print(scores.describe())
```

```text
count     4.000000
mean     78.750000
std       9.979145
min      68.000000
25%      72.500000
50%      78.000000
75%      84.250000
max      91.000000
dtype: float64
```

Eight numbers in one call: how many filled records there are, the mean, the
standard deviation, the minimum, the quartiles and the maximum. The `50%` row
is the **median**.

A mean far from the median meant there were extreme values — here they are
78.75 and 78.0, so the data is balanced.

## Series, list, array

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">list</span><span class="anat-body">any types mixed, processed with a loop, no labels</span></div>
    <div class="anat-row"><span class="anat-label">NumPy array</span><span class="anat-body">a single type, vectorised operations, no labels</span></div>
    <div class="anat-row"><span class="anat-label">pandas Series</span><span class="anat-body">a single type, vectorised operations, <b>labelled</b>, aware of missing values</span></div>
  </div>
</figure>

In the next section you will put several Series side by side and get a
**DataFrame** — that is the real table structure.

## Summary

- A **Series** is values plus an **index**. Without the index it would be a
  NumPy array.
- The index can be text: `scores["Mina"]`.
- Vectorised operations carry over from NumPy, with the labels along for the
  ride.
- **Alignment:** adding two Series matches on **labels**, not on order. A
  label that does not match gives `NaN`.
- **pandas skips missing values in calculations**, NumPy does not. So use
  `isna().sum()` to see how many there are.
- `fillna` and `dropna` both return a **new Series**.
- `value_counts()` is the first question you ask of a categorical column,
  `describe()` of a numeric one.
