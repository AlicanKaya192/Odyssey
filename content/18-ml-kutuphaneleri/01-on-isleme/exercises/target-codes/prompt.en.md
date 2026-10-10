`target_codes(shops, bought, new_shops)` should encode shops with
`TargetEncoder(random_state=0)`: `fit` with the training shops and the target
(`bought`), `transform` the new shops. Return the new shops' codes as a list
rounded to 3 places. Pass the data as `pd.DataFrame({"shop": ...})`. The
starter code computes the mean by hand: an unseen shop gives `nan` and the
mean of a shop with few records is not smoothed.

**Expected output:**

```
[0.651, 0.725, 0.6]
```
