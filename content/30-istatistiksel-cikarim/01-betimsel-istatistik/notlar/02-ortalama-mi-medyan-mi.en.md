Which one to report depends on the question. There is no single rule, but
three questions usually give the answer.

## 1. Do you care about a total?

If a **total** is asked, such as server cost, total sales or total time
spent, you need the mean: mean × number of people = total. The median cannot
do that calculation.

## 2. Are you describing the typical person?

For "how many minutes do our users usually stay?" the median is more honest
in skewed data. In this section the mean session length was
9.04 and the median 7.49 minutes: half of the users stay
shorter than 7.49 minutes.

## 3. Are the outliers real?

- If they are measurement errors (an app left open, a clock fault), clean
  the data first.
- If they are real behaviour (truly very long sessions), do not delete them;
  give both the median and the mean.

## Give both

Instead of a single number, this trio is often best in a report:

- the median (the typical value),
- the mean (for totals),
- a measure of spread: the IQR or the 95th percentile.

A large gap between the mean and the median is information in itself: it
says "the distribution is skewed, there are a few large values".

## Common mistakes

- Giving only the mean of skewed data and presenting it as "typical".
- Giving the mean and the standard deviation side by side and saying "most
  values are within the mean ± 2 deviations": that only holds for
  bell-shaped data.
- Mixing up the standard deviations of pandas and NumPy (`ddof`).
