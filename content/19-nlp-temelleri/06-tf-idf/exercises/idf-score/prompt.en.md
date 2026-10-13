`idf(df, n)` should compute IDF with scikit-learn's default formula and round it
to 3 places: `ln((1 + n) / (1 + df)) + 1`. `math.log` is the natural
logarithm.

**Expected output:**

```
1 7.216
10 5.511
100 3.294
1000 1.0
```
