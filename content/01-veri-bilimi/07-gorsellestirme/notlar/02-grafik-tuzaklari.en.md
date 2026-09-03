Most chart mistakes are **not code mistakes but communication mistakes.** The
code runs, a chart appears, and the reader draws the wrong conclusion.

## 1. The axis does not start at zero

When the values are 85, 87 and 88, matplotlib may start the axis at 84. The
3% difference between them looks like **three times** on screen.

This is the easiest way to produce a misleading chart, and it is usually
unintentional.

**On a bar chart** starting the axis at zero can be treated as a rule:

```python
ax.set_ylim(0, 100)
```

The reason: the **length** of a bar represents the value. Cut off the bottom
and the length is no longer proportional to the value.

The rule does not apply to line charts — there the subject is the trend, not
the absolute size.

## 2. A chart with no title and no labels

```python
ax.bar(x, y)
fig.savefig("chart.png")
```

What does this chart show? Is the y axis items, pounds or percent? The reader
has to guess.

A chart is drawn to be shown to someone; its title and axis labels are its
sentence. You are not writing three extra lines — **they are the lines you
have to write.**

Units in particular get forgotten: `set_ylabel("Sales (thousands)")`.

## 3. The wrong chart type

| Wrong | Why | Right |
|---|---|---|
| Joining categories with a line | It claims a continuity that does not exist | Bars |
| A time series as bars | The trend does not show | A line |
| A pie with more than five slices | The slices cannot be compared | Bars |
| A distribution as bars | The shape disappears | A histogram |

Pie charts are particularly problematic: the human eye is bad at comparing
angles. They work with two or three slices; beyond that bars are always more
readable.

## 4. Too much in one chart

A chart with eight lines is unreadable. Telling the colours apart and
tracking which is which becomes impossible.

Two fixes:

- **Emphasise:** draw the series you care about in colour and the rest in
  grey.
- **Split:** four small charts with `plt.subplots(2, 2)`.

The general rule: one chart says **one thing**. If you want to say two
things, draw two charts.

## 5. `plt.bar()` and `ax.bar()` get confused

```python
plt.bar(x, y)      # draws into "the current axes"
ax.bar(x, y)       # draws into a particular axes
```

The `plt` form keeps hidden state: "which axes is open right now". With one
chart it causes no trouble, but with two you lose track of which one you are
writing to.

**The `fig, ax` form** is always explicit and requires no guessing. The `plt`
form is common in tutorials because it is short; in your own code use `ax`.

## 6. Not closing figures in a loop

```python
for city in cities:
    fig, ax = plt.subplots()
    ...
    fig.savefig(f"{city}.png")
```

Twenty cities leave twenty open canvases and matplotlib warns you.

You have to close after saving:

```python
    plt.close(fig)
```

## 7. Scale deception: different axes

You put two charts side by side to compare them, but their axes have
different ranges. If one is 0-100 and the other 0-10, **the visual comparison
is meaningless**.

```python
fig, (left, right) = plt.subplots(1, 2, sharey=True)
```

`sharey=True` forces both charts onto the same axis.

## 8. An outlier crushes the whole chart

If one record is 10,000 and the rest are between 10 and 50, the histogram
looks like a single bar and the real distribution is squashed flat.

Three options:

- Examine the outlier separately and leave it out of the main chart (and
  **say so on the chart**).
- Make the axis logarithmic: `ax.set_yscale("log")`.
- Bound the axis: `ax.set_xlim(0, 100)` — but then the loss is invisible.

Whichever you choose, you have to tell the reader.

## 9. Colour blindness

Red and green are indistinguishable for around 8% of men. A "green is good,
red is bad" scheme carries no information for those readers.

Fixes: safe pairs like blue and orange, or **another signal** alongside the
colour (a pattern, thickness, a direct label).

For the same reason, a good test is whether the chart still reads when
printed in black and white.

## 10. Claiming causation

If the points in a scatter plot form a line, the two variables **move
together**. That does not mean one causes the other.

The classic example: ice cream sales and drownings rise together. Summer
causes both.

Writing "X increases Y" in a chart title is a **claim**; the chart does not
prove it. "The relationship between X and Y" is an honest title.

## 11. Cut-off labels

Long category names can overlap each other or be cut off at the edge.

Three fixes:

```python
ax.tick_params(axis="x", rotation=45)   # rotate
ax.barh(x, y)                            # horizontal bars
fig.savefig(..., bbox_inches="tight")   # do not trim the edge
```

Horizontal bars are usually the most readable with long names.

## 12. Trying to show the chart on screen

```python
plt.show()
```

There is no window in Odyssey; the call does nothing. With
`matplotlib.use("Agg")` the chart is drawn into memory and taken to a file
with `fig.savefig(...)`.

On your own machine `show()` works. But if you are producing a report,
saving to a file is more useful anyway: to regenerate the same chart you only
have to run the code.
