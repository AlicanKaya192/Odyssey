`vote_score(weights)` should combine logistic regression and a random forest with
`VotingClassifier(..., voting="soft", weights=weights)` and return the 5-fold
mean accuracy (3 places). The starter code uses `"hard"` (majority vote); in
soft voting the probabilities are averaged with the weights.

**Expected output:**

```
0.904
0.907
```
