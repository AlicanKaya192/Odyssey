A group report has three columns: **how many, the average, the spread.**
You will produce all three.

**What you need to do:**

1. Group by city and compute the count, mean and standard deviation of
   `score`, rounded to two decimals.
2. Print the table.
3. Print the mean (two decimals) and the median of the whole data **side by
   side**.
4. Print the name of the **smallest group**.

**Expected output:**

```
        count  mean    std
city
Ankara      3  80.0   9.17
Bursa       2  48.0   4.24
Izmir       3  79.0  15.13
71.62 76.0
Bursa
```

**Read the output:**

- Bursa's average is low, but there are **two people**; that is not a
  conclusion.
- Izmir's `std` is 15.13 against Ankara's 9.17. Two groups with almost the
  same average, but Izmir is far more scattered — there may be two different
  kinds of student there.
- The overall mean is 71.62 and the median 76. The mean is below the median,
  so there are low scores at the bottom.

Three lines of code, three separate findings. That is why `agg` is preferred
over separate calls.
