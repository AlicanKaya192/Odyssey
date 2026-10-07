What happens if the stock counts of a warehouse are forced into `int8`?
Find the values that broke, then shrink the right way.

**What to do:**

1. Build the series `stock = pd.Series([90, 120, 250, 300, 40])`.
2. Take the result of `stock.astype("int8")` as `forced` and print it as a
   list.
3. Print how many values broke: `(forced != stock).sum()`.
4. Print the **original** values of the ones that broke, as a list.
5. The right way: print the type and the list of
   `pd.to_numeric(stock, downcast="integer")` on one line.

**Expected output:**

```
[90, 120, -6, 44, 40]
2
[250, 300]
int16 [90, 120, 250, 300, 40]
```

`astype` broke them silently; `downcast` picked the type the values fit into
(`int16`).
