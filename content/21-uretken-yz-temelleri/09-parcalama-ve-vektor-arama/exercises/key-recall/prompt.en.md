`key_recall(results, keys)` should take, for every question, the list of
chunks found (`results[i]`) and the correct answer phrase (`keys[i]`). A
question counts as "found" if the phrase appears in one of the chunks. Return
the share found as a `float` rounded to 2 places.

**Expected output:**

```
0.67
```
