Split the data into training and test sets: **the right way**, and
measure how badly a random split goes wrong.

The data is already in date order. To split by time, cutting by position is
enough: the first 80% for training, the rest for testing.

**What to do:**

1. Read `store_sales.csv`.
2. Find the number of training rows with `int(len(table) * 0.8)`. Use `iloc`
   to make the first part `train` and the rest `test`.
3. Print the last training date, the first test date and the number of test
   rows on one line.
4. Is the largest training date smaller than the smallest test date? Print
   the result (`True` / `False`).
5. Now try the wrong way: `train_test_split(table, test_size=0.2,
   random_state=0)`. In the random test set, how many days fall **before the
   latest date** of the random training set? Print this count and the number
   of test rows on one line.

**Expected output:**

```
2024-05-25 2024-05-26 220
True
219 220
```

With a random split nearly every test day comes before a day the model saw
in training. The model is tested having seen the future.
