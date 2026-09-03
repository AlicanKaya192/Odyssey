In section 00 you found the **single** nearest neighbour. Now you will look
at `k` neighbours and hold a **vote** — and see that `k` changes the answer.

**What you need to do:**

1. Compute the Euclidean distance from the new point to every point, rounded
   to two decimals.
2. Sort the `(distance, label)` pairs **from small to large**.
3. Print the sorted distances as a list.
4. With `k` set to **1, 3 and 5** in turn:
   - take the labels of the nearest `k` neighbours
   - decide the winner by majority
   - print one line: **k, the labels, the winner**

**Expected output:**

```
[0.71, 1.0, 2.92, 3.61, 4.03, 4.24, 4.3, 4.61]
1 ['A'] A
3 ['A', 'B', 'B'] B
5 ['A', 'B', 'B', 'A', 'B'] B
```

**Look at the second and third lines: the answer changed.**

`k=1` says **A** — the nearest neighbour is 0.71 away and its label is A.

`k=3` says **B** — two of the three neighbours are B.

The same data, the same point, a different result. So `k` is not a small
detail; it is **the model itself.** How to choose it comes in the later
exercises.

**This is also why an odd number is chosen:** with `k=2`, one neighbour A
and one B, the votes would tie. In binary classification an odd `k` is a
habit for that reason.
