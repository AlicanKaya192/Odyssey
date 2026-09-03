You will build a classifier in its simplest form: **a new point resembles
its nearest neighbour.**

You have five labelled points and one new point whose label is unknown.

**What you need to do:**

1. Compute the distance from the new point to every point (Euclidean: the
   square root of the sum of the squared differences).
2. Print the distances **sorted from small to large**, to two decimals, as a
   list.
3. Print the label of the **nearest** point.
4. Print the labels of the **three nearest** points as a list.

**Expected output:**

```
[0.71, 1.12, 5.66, 6.73, 7.11]
B
['B', 'B', 'A']
```

**What you built has a name: KNN.** With `k=1` you take the nearest
neighbour's label; with `k=3` you look at the nearest three and follow the
majority. The last line came out `['B', 'B', 'A']`: two out of three, so
**B** again.

You choose `k`, not the model — that is called a **hyperparameter**. A small
`k` is sensitive to noise, a large one blurs the boundaries.

**A warning:** this method works on distance. If one column ran 0 to 1 and
another 0 to 100,000, the large column alone would decide the distance. That
is section 6.
