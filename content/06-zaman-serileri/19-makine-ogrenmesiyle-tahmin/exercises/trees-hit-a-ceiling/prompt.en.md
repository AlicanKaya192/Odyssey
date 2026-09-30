See why gradient boosting falls behind on a growing series, and fix it by
changing the target.

**What to do:**

1. Print the highest `y` in the training data and the highest `y` in 2024 on
   one line.
2. Fit `HistGradientBoostingRegressor(random_state=0)` on the level and
   forecast 2024. Print its highest forecast (one decimal).
3. Print the test error for the whole of 2024 and for December 2024 only, with
   two decimals, on one line.
4. Turn the target into a difference: `target = table["y"] - table["lag7"]`.
   Remove `lag7` from the features; subtract `lag7` from the columns `lag1`,
   `lag2`, `lag14`, `mean7`, `mean28` too (so that the model never sees the
   raw level). Fit the same model on this table.
5. Turn the forecast back into a level (model output + `lag7`) and print the
   two errors of step 3 for this model.
6. Print the highest forecast of the new model (one decimal).

**Expected output:**

```
462 503
415.7
14.63 22.47
11.74 10.87
494.5
```

The highest forecast of the tree fitted on the level is below even the highest
value it saw in training; that is why the error in December is large. With the
difference as the target the model learns "how much does it change on last
week"; the level is carried by `lag7` and the forecast can now go past the
ceiling of the training data.
