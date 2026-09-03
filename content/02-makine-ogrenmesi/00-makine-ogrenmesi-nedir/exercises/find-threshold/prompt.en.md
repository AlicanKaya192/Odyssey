In this exercise you will **train** a model — without a library.

You have ten students' scores and whether they passed. You do not know what
the pass mark was; you are going to **find it from the data.**

**What you need to do:**

1. Try every threshold from 30 to 100 in steps of five.
2. For each one, produce a prediction: 1 if the score is at or above the
   threshold, 0 otherwise.
3. Count how many predictions match reality and compute the proportion.
4. Print the threshold that gives the **highest** proportion and that
   proportion, side by side (two decimals).

**Expected output:**

```
55 0.9
```

**That is learning itself.** What you did was search for a parameter with a
loop; linear regression does the same job — except the numbers it searches
for are a slope and an intercept, and the search is done cleverly.

The model stops at 90% rather than 100%: the data has someone who scored 66
and failed and someone who scored 60 and passed. **No threshold can get both
right.** Real data is like that; a perfect score is usually the sign of a
mistake.
