In the previous exercise you saw the test column jump. Now you will measure
where that jumping comes from.

The model is fixed. The data is fixed. **The only thing changing is the
randomness of the split.**

**What you need to do:**

1. Prepare the data (read, drop the gaps, encode) but **do not split it**.
2. Split five times, with `random_state` running from **0 to 4**.
3. Train a linear regression each round and measure the test MAE. Round it
   to two decimals and collect it in a list.
4. Print the list as it is.
5. Print the **lowest, the highest and the difference** side by side.

**Expected output:**

```
[16.16, 16.95, 17.07, 19.68, 21.56]
16.16 21.56 5.4
```

**The same model, the same data, five different answers.**

The lowest is 16.16 and the highest 21.56. The difference is **5.40** —
about a third of the number itself.

Think about that in a report: someone who wrote `random_state=0` says "my
model's error is 16.16" and someone who wrote `random_state=4` says "21.56".
Both are honest, and both describe the same model.

**This is a warning that sits above every number you measured in earlier
sections.** A result from a single split is an **estimate**, not a precise
measurement. Writing `random_state=42` makes the result reproducible; it
does not make it more accurate.

Comparing two models it is more dangerous still: does the 2-unit gap between
them come from the model or from the split? As things stand you cannot say.

The fix is in the next exercise.
