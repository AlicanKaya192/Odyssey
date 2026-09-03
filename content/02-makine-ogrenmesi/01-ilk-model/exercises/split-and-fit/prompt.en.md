Now you will build the whole flow with a real file: read, split, train,
measure.

The `homes.csv` file next to this exercise holds 40 houses; its columns are
`area`, `rooms`, `age` and `price`.

**What you need to do:**

1. Import everything you need and read the file.
2. Take the `area` column as a **table** into `X` and the `price` column as
   a **column** into `y`.
3. Split the data: **a quarter for testing**, `random_state=42`.
4. Print the training and test counts **side by side**.
5. Train the model; print the **slope and intercept** it learned side by
   side (two decimals).
6. Print the **mean absolute error** on the test set (two decimals).

**Expected output:**

```
30 10
2.92 -1.48
18.5
```

**Three things to watch:**

- **Double** brackets for `X`, **single** for `y`. Single brackets give you
  the `Expected 2D array` error.
- `train_test_split` returns in the order `X_train, X_test, y_train,
  y_test`. Mix it up and you get no error — you get a wrong result.
- Without `random_state=42` every run gives different numbers and the check
  fails. That is not a restriction but the point of the exercise:
  **randomness that is not fixed means results that cannot be repeated.**

The `-1.48` is an intercept and reads like the price of a zero square metre
house — meaningless. No harm done: an intercept's job is to place the line
correctly, not to be interpreted on its own.
