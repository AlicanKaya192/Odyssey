`phishing_score(mail, weights, threshold)` should compute an e-mail's
warning score: the points in `weights` of every sign whose value in `mail`
is `True` are added up. A sign missing from `mail` counts as `False`.

Return the tuple `(score, decision)`: the decision is `"report"` if the
score is equal to or greater than `threshold`, otherwise `"ok"`.

**Expected output:**

```
(5, 'report')
(0, 'ok')
```
