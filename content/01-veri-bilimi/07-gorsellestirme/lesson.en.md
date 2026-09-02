# Visualisation

So far you have answered with numbers: an average of 87, three cities, Mina
at the top. For some questions that is enough. For others you have to
**look**.

```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
```

`plt` is a convention like `pd` and `np`.

**What is that `matplotlib.use("Agg")` line?** It draws the chart into memory
rather than showing it on screen. Exercises in Odyssey have no window, so
that line is needed here. On your own machine you do not write it.

## Why a chart?

Look at the same data two ways:

```text
city    average
Ankara     87.0
Izmir      71.3
Bursa      69.0
```

To read this table you have to compare three numbers. In a bar chart the same
information arrives **at a glance**: Ankara is clearly ahead and the other
two are close to each other.

At three rows the difference is small, at thirty it is large, and at three
hundred reading the table is impossible.

<figure class="fig">
  <div class="versus">
    <div class="versus-side">
      <h4>A table</h4>
      <p>Exact values. It answers "what exactly is Ankara?"</p>
    </div>
    <div class="versus-side">
      <h4>A chart</h4>
      <p>Relationships and patterns. It answers "which one stands out, is there a trend?"</p>
    </div>
  </div>
  <figcaption>Neither replaces the other. A report usually has both: the chart draws attention, the table confirms.</figcaption>
</figure>

## Figure and axes

matplotlib has two concepts:

```python
fig, ax = plt.subplots()
```

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">fig</span><span class="anat-body">the canvas — what gets saved and sized</span></div>
    <div class="anat-row"><span class="anat-label">ax</span><span class="anat-body">the drawing area — bars, lines and labels go in here</span></div>
  </div>
</figure>

One canvas can hold several drawing areas:

```python
fig, (left, right) = plt.subplots(1, 2)
```

In tutorials you will also see short forms like `plt.bar(...)`. Those work
too, but they keep a hidden "current axes" behind the scenes; with two charts
you lose track of which one you are writing to. **The `fig, ax` form is
explicit and does not get confused.**

## Bar chart

For comparing categories:

```python
data = pd.DataFrame({"city": ["Ankara", "Izmir", "Bursa"], "score": [87, 71, 69]})

fig, ax = plt.subplots()
ax.bar(data["city"], data["score"])
ax.set_title("Average score by city")
ax.set_xlabel("City")
ax.set_ylabel("Score")
fig.savefig("chart.png")
```

Those three lines of labelling look optional but are not: **a chart without a
title and axis labels is an unfinished sentence.** Whoever sees it does not
know what they are looking at.

## Line chart

For change over time:

```python
fig, ax = plt.subplots()
ax.plot(months, sales, marker="o")
```

A bar compares **categories**, a line shows **how something changed**. You
could draw months as bars, but a line tells the trend better.

`marker="o"` marks the actual measurements — the line between them is a
guess, the points are the data.

## Histogram

For the **distribution** of one numeric column:

```python
fig, ax = plt.subplots()
ax.hist(data["score"], bins=10)
```

A histogram splits the values into ranges and shows how many records fall in
each. The difference from a bar chart: there you have categories, here
**numeric ranges**.

`describe()` gave you the mean and the median; a histogram shows the
**shape**. Are there two peaks, is it skewed, where are the extremes — none
of that is visible in the numbers.

The number of `bins` matters: too few and the detail disappears, too many and
you are looking at noise.

## Scatter plot

For the **relationship** between two numeric columns:

```python
fig, ax = plt.subplots()
ax.scatter(data["hours"], data["score"])
```

Each point is a record. If the points form a line, the two variables move
together.

**Careful:** moving together does not mean one causes the other. Ice cream
sales and drownings rise together; summer causes both.

## Labels are not negotiable

```python
ax.set_title("Average score by city")
ax.set_xlabel("City")
ax.set_ylabel("Score (0-100)")
```

A chart is drawn to be shown to someone else. The title says what they are
looking at, the axis labels say in what units.

Units matter especially: does an axis labelled "Sales" mean items, pounds or
thousands of pounds? The reader is left guessing.

## Saving

```python
fig.savefig("chart.png", dpi=150, bbox_inches="tight")
```

- `dpi` is the resolution; 150 is a good value for a report.
- `bbox_inches="tight"` trims the excess margin so long labels are not cut
  off.

There is also `plt.show()`, but that opens a window; it does not work in
Odyssey, and saving to a file is more useful for reporting anyway.

## The pandas shortcut

pandas has its own `plot` method that calls matplotlib behind the scenes:

```python
data.plot(kind="bar", x="city", y="score")
```

Handy for a quick look. But it gives you little control; when you need a
title, colours and layout you go back to the `fig, ax` form.

## Which chart?

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">Bar</span><span class="anat-body">compare categories — sales by city</span></div>
    <div class="anat-row"><span class="anat-label">Line</span><span class="anat-body">change over time — sales by month</span></div>
    <div class="anat-row"><span class="anat-label">Histogram</span><span class="anat-body">the distribution of one column — how the scores are spread</span></div>
    <div class="anat-row"><span class="anat-label">Scatter</span><span class="anat-body">the relationship between two columns — study hours against score</span></div>
  </div>
</figure>

Choosing the wrong chart is as bad as a wrong answer: joining categories with
a line says there is a continuity between them that does not exist.

## A warning: when the axis does not start at zero

matplotlib scales the axis to the range of the data. If the values are 85, 87
and 88, the axis may start at 84 and **small differences look enormous**.

This is the easiest way to produce a misleading chart without meaning to.
Starting the axis at zero is a good habit for bar charts:

```python
ax.set_ylim(0, 100)
```

The rule does not apply to line charts — there the subject is the trend, not
the absolute size.

## Summary

- **A chart shows relationships, a table gives values.** Neither replaces the
  other.
- `fig, ax = plt.subplots()` — `fig` is the canvas, `ax` the drawing area.
  The explicit form does not get confused.
- **Bar** for categories, **line** for time, **histogram** for a
  distribution, **scatter** for a relationship between two variables.
- **A title and axis labels are required**; without units the reader guesses.
- Save with `fig.savefig(...)`; `dpi` and `bbox_inches` are worth using.
- In Odyssey you need `matplotlib.use("Agg")` — there is no window.
- **Start the axis at zero on a bar chart**, or small differences look large.
- Moving together is **not causation**.
