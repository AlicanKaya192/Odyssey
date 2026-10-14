`groups(results)` should put every `[key, answer]` pair into one of the
lesson's four groups and return the counts `[correct, abstain ok, wrong,
missed]`. If `key` is `None` the question has no answer: if the answer is
`NOT_FOUND` it is abstain ok, otherwise wrong. If there is a `key`: if the
answer is `NOT_FOUND` it is missed, if `key` appears in the answer it is
correct, otherwise wrong.

**Expected output:**

```
[1, 1, 1, 1]
```
