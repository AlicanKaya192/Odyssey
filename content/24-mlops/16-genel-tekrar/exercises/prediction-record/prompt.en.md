Write the function `prediction_record(customer_id, score, version, threshold)` that joins the serving and monitoring sections. It should return a dictionary:

- `"id"`: the customer id, `"version"`: the model version.
- `"score"`: the score, rounded to three digits.
- `"decision"`: `"offer"` if the score is at least `threshold`, otherwise `"no offer"`.

**Expected output:**

```
C06-00001 3
0.426 offer
no offer
```
