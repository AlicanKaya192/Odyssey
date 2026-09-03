A trained model lives in memory. When the program closes, it is gone.

In this exercise you will save the pipeline to disk, load it back, and
produce predictions from **raw data** — raw data with missing values.

**What you need to do:**

1. Prepare, split the data, build the pipeline and fit it.
2. Save it as `model.joblib` with `joblib.dump`. Print whether the file is
   larger than 1000 bytes.
3. Load it back with `joblib.load`.
4. Print whether the loaded model's predictions on the test set are **the
   same** as the original model's.
5. Build a `DataFrame` of three new subscribers:
   - Bursa / basic / tenure 3 / monthly 140.0 / support 4
   - Izmir / pro / tenure 48 / monthly 45.0 / support 0
   - **city and monthly fee unknown** / plus / tenure 20 / support 1
6. Print the loaded model's predictions for these three rows and their
   positive-class probabilities, on separate lines (probabilities to three
   decimals).

**Expected output:**

```
True
True
[1, 0, 0]
[0.993, 0.007, 0.466]
```

**Do not miss what the third row means.** You handed it a raw dict: no
`city`, no `monthly`. Unscaled numbers, unencoded text.

The model worked. Because what was saved is not just the coefficients but
**the whole pipeline**:

- The numeric columns' median, computed during training
- The text columns' mode, computed during training
- The categories the encoder learned
- The scaler's mean and standard deviation
- The model's coefficients and the column order

**With a hand-prepared model that row would have been a crash** — or worse,
it would have recomputed the median and quietly produced a wrong
prediction.

**Look at the probabilities:** the first subscriber is at 0.993 (Bursa +
basic + short tenure + many support calls — four risk factors at once), the
second at 0.007 (Izmir + pro + long tenure + no support), and the third at
0.466 — **undecided**, because two of its columns are missing and the model
filled them with average values.

That third number is an honest answer: "I do not know enough about this
subscriber."

**What the file does not carry:** the library versions, the training data,
the decision threshold you chose, and the scores you measured. A text file
beside it covers those — the second note explains how to write it.
