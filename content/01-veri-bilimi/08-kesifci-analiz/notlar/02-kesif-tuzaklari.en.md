None of the mistakes in this note are code mistakes. The code runs, a number
comes out, and **the wrong conclusion is drawn from the number.**

## 1. Reading an average without the spread

Two groups both average 70. In the first everyone is between 68 and 72; in
the second half are on 40 and half on 100.

The same average, two completely different situations. Without asking for
`std`, an average is half the information:

```python
data.groupby("city")["score"].agg(["count", "mean", "std"])
```

## 2. Taking a small group seriously

```text
        count  mean
Bursa       2  48.0
```

There is nothing to say about the average of a group of two. One person more
or less and the number would change completely.

A rough threshold: **below 30**, read the number as a hint rather than a
conclusion. And always write the group size in the report.

## 3. The average reversing within the groups

This trap has a name: **Simpson's paradox**.

```text
team
A    74.0
B    61.0
```

Team A looks ahead. But split by difficulty:

```text
team  level
A     easy     80.0
      hard     50.0
B     easy     85.0
      hard     55.0
```

**B is better at both levels.** The reason is the mix: A mostly solved the
easy questions and B mostly the hard ones.

The overall average is not lying, but it is **answering the wrong
question.**

The defence: when you find a difference between groups, ask "is something
else different about these groups too" and break it down by that column as
well.

## 4. Mistaking correlation for causation

The most frequently repeated mistake.

`hours` and `score` correlate at 0.98. But in the same data `age` and
`hours` correlate at -0.89: the older people studied less. Is it age or
study hours that lowers the score? The data does not say.

Three possibilities are always open:

- A causes B.
- B causes A.
- C causes both.

An analysis cannot separate the three; separating them takes an experiment.

## 5. Saying "no relationship" because the correlation is 0

Correlation measures a **linear** relationship. With a U-shaped
relationship the correlation comes out near 0 while the relationship is
very much there.

That is why you look at a **scatter plot** before the number. Completely
different patterns can produce the same correlation value.

## 6. Deleting an outlier without thinking

```python
data = data[data["score"] < 1000]
```

That line is a decision. The question to ask before deleting a value: **is
it an error, or a genuine extreme?**

- An age of 200 → an error, it can go.
- A salary 40 times the average → possibly the chief executive. Delete it
  and you skew the data.

Extremes are sometimes the most interesting part of the data: fraud
detection is built entirely on them.

## 7. Assuming missing values are random

`dropna()` looks like an easy fix. But if the blanks are not randomly
distributed, **the remaining data no longer represents anything.**

In a survey it is usually the high earners who leave the income question
blank. Drop the blanks and the average income comes out lower than it is —
and nobody notices.

The question is not "how many are blank" but **"why are they blank"**.

## 8. A count where a percentage belongs, and the reverse

"20 records are missing" is not information. 20 missing out of 100 rows is
serious; 20 out of 100,000 is nothing.

The same in the other direction: "a 50% increase" says nothing if it went
from 2 to 3. **The percentage and the raw count go together.**

## 9. Searching until something turns up

Compare twenty columns with each other and one of them will show a high
correlation by chance. What you found is not in the data, it is in your
searching.

The honest way: **ask the question first**, then look. Note the questions
that arise while looking as "this needs separate confirmation"; do not write
them up as findings.

## 10. Using the mean where the median belongs

In right-skewed data like income, duration or price, the mean does not
describe reality. A few large values pull it up, and the "average user" you
describe does not exist in the data at all.

If `mean` and `50%` are far apart in `describe()`, **report the median**.

## 11. A type being silently wrong

If the `score` column is of type `str`, `sort_values()` runs but sorts in
**text order**: `"100"` comes before `"9"`.

No error, no warning, wrong result. That is why step two is `dtypes`.

## 12. Turning a finding into a claim

The last sentence of a report is the most dangerous place:

| Read off the data | Carries an extra claim |
|---|---|
| "In this data X and Y move together" | "X increases Y" |
| "The two Bursa records are low" | "Scores are low in Bursa" |
| "Sales rose in January" | "The campaign worked" |

The sentences on the right are not necessarily false — but **the data does
not prove them.** The honesty of an analysis lies exactly in keeping that
difference.
