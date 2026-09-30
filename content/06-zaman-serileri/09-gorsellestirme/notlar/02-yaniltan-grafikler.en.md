A chart can say something false without containing a single wrong number.
Six ways this most often happens with time series, and the fix for each.

## 1. Two separate vertical axes

`ax.twinx()` lets you put two series of different scales on one chart. The
problem: **you** choose the range of each axis, and by adjusting the ranges
you can make the two lines overlap or sit apart as much as you like. The same
data can be drawn as "they move together" and as "they are unrelated".

The fix: **index** the two series (both starting at 100) or draw **two
stacked panels**. If you want to see the relationship, use a scatter plot and
a correlation.

## 2. A truncated vertical axis

Start the axis at 280 and end it at 300 and a 3% wobble looks like a cliff.
On a bar chart the **length** of the bar tells the value, so the axis must
start at zero. On a line chart zero is not mandatory, but know that you chose
the range and give the reader a sense of the level (state the percentage
change, or add a small panel with zero).

## 3. A chosen time range

The same series can look "rising" or "falling" depending on the start date. A
chart starting in December always shows a fall; one starting in May always a
rise.

The fix: show at least one full seasonal cycle (preferably two); you should
be able to say why the start and the end are where they are. When comparing
two points of a seasonal series, compare the same season.

## 4. Too much smoothing

A 365-day moving average makes any series look calm and steady. A break, an
outlier day, a rise in volatility all vanish under the smooth line.

The fix: keep the raw series behind, however faintly; write the window length
in the title or the legend. Remember that a trailing mean shows turning
points late (Section 07).

## 5. A growing series on a linear axis

For a series that grows by a percentage, a linear axis exaggerates the last
years and squeezes the first ones into a flat line. Going from 100 to 200 and
from 1000 to 2000 is the same growth (a doubling), but on a linear axis the
second is ten times steeper.

The fix: `ax.set_yscale("log")`. The reverse is a mistake too: a logarithmic
axis hides absolute differences; where **the amount itself** matters, such as
a budget or stock levels, a linear axis is right.

## 6. Gaps joined up

If missing days are not there as rows, the line joins the two neighbouring
points and the data looks continuous. A five-day outage sits there as a
straight segment that looks "measured".

The fix: `asfreq` before plotting; let the line break.

## Before you publish

1. Does the title say what is shown? ("Daily sales, 2022–2024")
2. Is the **unit** of the vertical axis written?
3. Is the frequency clear (daily, weekly mean, monthly total)?
4. If there is smoothing, is the window length stated?
5. Does a bar chart's axis start at zero?
6. Is missing data joined up by a line?
7. Are the start and end dates justified?
8. Can the colours be told apart by someone who is colour-blind? Change the
   line style or the marker too.
9. Does the chart answer one question? If two, make two charts.
