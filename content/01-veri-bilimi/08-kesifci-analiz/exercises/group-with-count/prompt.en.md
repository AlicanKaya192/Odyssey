A group average is not read **on its own**. This exercise shows you why.

**What you need to do:**

1. Group by city and compute **both the count and the mean** of `score`,
   rounded to one decimal.
2. Print the table.
3. Print how many people are in the **smallest group**.
4. Print the city with the **highest** average.
5. Print the city with the **lowest** average.

**Expected output:**

```
        count  mean
city
Ankara      4  76.5
Bursa       2  48.0
Izmir       4  81.5
2
Izmir
Bursa
```

**Look at the output:** Bursa averages 48 while the others are 76 and 81.
The gap looks large.

But the `count` column shows **2** next to Bursa. There is nothing to say
about the average of a group of two — one person more or less and the number
would change completely.

That is the reason for writing `agg(["count", "mean"])`. Had you asked for
the average alone, you would not have seen the trap.

In a report this is written as "the two Bursa records are low" — not "scores
are low in Bursa".
