The results of two systems on the same questions (`"correct"`,
`"abstain ok"`, `"missed"`, `"wrong"`) are in two lists. Scores: `correct` and
`abstain ok` 1, `missed` 0, `wrong` −1. `compare(a, b)` should count a question
as "improved" if b's score is higher than a's and "worsened" if lower, and
return `[improved, worsened]`.

**Expected output:**

```
[2, 1]
```
