`false_share(n_ideas, share_work, power, alpha)` should compute with expected
counts: false alarms from ideas that do not work
`n_ideas * (1 - share_work) * alpha`, true results from ideas that work
`n_ideas * share_work * power`. Return the share of false alarms among
significant results with 3 places. The starter code assumes this share is
`alpha`; it is not.

**Expected output:**

```text
0.726
0.36
```
