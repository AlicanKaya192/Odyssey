`cv_mean(C)` should build a Pipeline from `TfidfVectorizer()` and
`LogisticRegression(C=C, max_iter=1000)`, measure macro F1
(`scoring="f1_macro"`) on the reviews with **5-fold** cross-validation and
return the mean with 3 places.

**Expected output:**

```
0.828
0.84
```
