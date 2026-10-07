A sample shrinks the numbers but must not change the question. Each of these
mistakes leads to a sample that does not represent the whole.

## 1. The first N rows

`head(10_000)` on orders in time order is the first four days of the year.
Files are often written in some order (time, customer, region); the first
rows are only the beginning of that order. Always choose at random.

## 2. Thinking a big sample fixes bias

As a sample taken with a biased method grows, the bias stays; it only looks
more certain. "The first million rows" are still just the first rows.

## 3. Looking for a rare event with a sample

An event that happens once in a thousand appears on average ten times in a
one percent sample of a million rows; sometimes not at all. For rare events
such as fraud, failures and complaints, look at all the data or sample those
events separately.

## 4. Comparing a small group with a simple sample

In a random sample of 1 600 rows Trabzon got 75 orders; its estimate moved
about three times as much as Istanbul's. If you will compare groups, use a
stratified sample.

## 5. Forgetting the seed

Without `random_state` every run picks different rows; the result cannot be
repeated and debugging gets harder. Give a seed and write it in your report.

## 6. Filtering before sampling, or the other way round

"One percent of the Izmir orders" and "the Izmir orders in a one percent
sample" are not the same question. In the second, only about 1 300 rows are
left for Izmir. Write down what you want in a sentence first.

## 7. Taking an approximate result as exact

On this track `approx_count_distinct` counted 245 461 customers as 219 479
(10.6 percent short). Say "approximately" when you report an approximate
number; do not use it for work such as invoices and accounting.

## 8. Working out the standard error with the wrong n

In the standard error, n is the size of the **sample**, not of all the data.
A sample of 10 000 from a million rows: n = 10 000.
