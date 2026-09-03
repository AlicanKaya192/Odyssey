In this section's examples leakage barely moved the number. Now you will see
where it moves a great deal.

You have 80 rows and 300 columns. **Every value is random** — none of them
has any relationship with the target. A correctly built model should find
nothing here.

**What you need to do:**

**The leaky path:**

1. Compute each column's relationship with the target (the absolute
   correlation) **by looking at all the data**.
2. Select the five highest columns.
3. **Then** split (`random_state=42`), train a linear regression and compute
   R² on the test set. Print it to three decimals.

**The clean path:**

4. **Split first** (the same `random_state`).
5. Compute the relationships on the **training data only** and select the
   five columns from that.
6. Train the same model and compute R² on the test set. Print it to three
   decimals.

**Expected output:**

```
0.442
-0.273
```

**The second number is the correct one.** A negative R² means the model is
worse than the baseline — and that is exactly what should happen here,
because there is nothing in this data to learn.

**The first number is fiction.** 0.442 makes it look as though a model
exists. Yet the only thing done differently was selecting the columns **by
looking at all the data**.

**How it happens:** among 300 random columns, some happen to agree with the
target values in the test rows. When the selection looks at all the data,
those are precisely the columns it picks — the selection criterion rewards
them. The model is then built from those columns and measured on that same
test data, and it looks good.

**The model is worth nothing.** With new data the coincidental agreement
disappears.

**That number can go on a slide and nobody will notice.** This is what makes
leakage dangerous: no error, no warning, just a number prettier than
expected.

**A practical rule:** when a result is much better than you expected, do not
celebrate first — look for leakage first. R² 0.99 or 100% accuracy is
usually not an achievement but a symptom.
