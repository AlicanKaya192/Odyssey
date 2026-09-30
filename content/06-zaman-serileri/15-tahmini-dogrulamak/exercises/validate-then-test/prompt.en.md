What should `k` be in the "mean of the last `k` weeks" method? Choose the
setting on the validation experiments and measure the result on the test
experiments.

In the starter code `weeks_mean(train, h, k)`, `cuts` (the 13 cut days) and
`score(k, some_cuts)` (the mean MAE over the given cuts) are ready.

**What to do:**

1. Split the cuts in two: the first 10 are validation, the last 3 the test.
   That is, `validation = cuts[:10]`, `test = cuts[10:]`.
2. Compute the validation MAE for `k = 1..8` and print the values with two
   decimals as a list.
3. Find the best `k` on validation; print `k`, its validation MAE and the test
   MAE **of the same `k`**, with two decimals, on one line.
4. If you cheated: print the `k` that looks best on the test and its test MAE
   on one line.
5. Print the difference between the two test MAEs with two decimals.

**Expected output:**

```
[16.61, 15.84, 15.16, 15.2, 15.4, 15.82, 15.86, 16.17]
3 15.16 22.97
1 22.42
0.56
```

By validation `k = 3` is chosen; the honest result is its error on the test.
Choosing the `k` that looks best on the test and reporting that would make the
error look smaller than it is: you would have made that decision by looking at
the test data, and in real use that advantage would not be there. The test
coming out markedly harder than validation is a finding too: the last
experiments fall in the most volatile quarter of the year.
