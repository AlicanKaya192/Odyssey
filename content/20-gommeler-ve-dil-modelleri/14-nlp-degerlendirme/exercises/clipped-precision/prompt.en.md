`clipped_precision(candidate, reference, n)` should compute one step of BLEU:
the share of the candidate's `n`-word groups that also appear in the
reference; each group counts at most as many times as it appears in the
reference. 3 places; `0.0` if the candidate has no groups.

**Expected output:**

```
0.75
0.25
0.667
```
