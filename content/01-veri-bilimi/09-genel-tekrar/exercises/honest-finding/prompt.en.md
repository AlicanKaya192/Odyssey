We have how many minutes three teams took to finish a job. The question
asked: **which team is slow?**

**What you need to do:**

1. Find the outliers with the IQR rule and print them **as a list**.
2. Print the mean (two decimals) and the median of all the data **side by
   side**.
3. Print the count and mean by team, rounded to one decimal.

**Expected output:**

```
[240]
51.5 30.5
      count  mean
team
A         4  31.0
B         4  82.2
C         2  31.0
```

**Now read the output — that is the real exercise.**

At first glance team B looks terrible: an average of 82 against 31 for the
others.

But look at the first line: there is **a single record of 240 minutes** in
the data, and it belongs to team B. Take it out and B's other three values
are 27, 33 and 29 — no different from the other teams.

The mean is 51.5 while the median is 30.5. The gulf between them comes from
one value.

**Notice team C too:** its average is 31, but there are only two records.

The honest finding: *team B's average is lifted by a single 240-minute
record; with that record removed, all three teams are similar. What that 240
is needs investigating — it could be a measurement error, or a genuinely long
job.*

Saying "team B is slow" is something this data does not say.
