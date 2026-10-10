`best_c(cs)` should run `GridSearchCV(LogisticRegression(), {"C": cs}, cv=5)` on the
training data in the starter code and return `[best_C, best_score]` (score
with 3 places).

**Expected output:**

```
[0.1, np.float64(0.831)]
```
