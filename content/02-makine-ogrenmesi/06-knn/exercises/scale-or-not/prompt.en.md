In section 04 you saw that scaling affects KNN. In this exercise you will
measure how large that effect is — and the result is probably sharper than
you expect.

`customers.csv` holds 200 customers: `age` (18-70), `income`
(12,000-200,000), `visits` (1-50) and the target `churn` (did they leave).

**What you need to do:**

1. Read the file, take the three columns into `X` and `churn` into `y`.
2. Split: a quarter for testing, `random_state=42`, **`stratify=y`**.
3. Print the training and test counts side by side.
4. Build the **baseline**: predict the most frequent class for every test
   record and print its accuracy to three decimals.
5. Train two KNNs (`n_neighbors=5`): one on the **raw** data, one on the
   **scaled** data. Print the two accuracies side by side.
6. Print `worse` if the raw KNN is **below** the baseline, `better`
   otherwise.

**Expected output:**

```
150 50
0.7
0.64 0.92
worse
```

**The last line is what this exercise is really about.**

Unscaled, KNN gives **0.64**. The baseline is **0.70**. So the model is
**worse** than a one-line rule saying "tell everyone the most frequent
class".

After scaling, the same model gives **0.92**.

**Why so severe:** in a distance computation the gap between two customers
in `income` can be 100,000 while in `visits` it is at most 49. Once squared
and summed, the second does not even show up. Unscaled, KNN is really
**only looking at income**; the other two columns were handed to the model
and go unused.

**The lesson:** for KNN, scaling is not an improvement but a **compulsory
step**. Skip it and the result can be worse than not building a model at all
— and there is no way to notice that without looking at the baseline.
