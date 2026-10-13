`brevity_penalty(candidate_len, reference_len)` should return `1.0` if the
candidate is not shorter than the reference, otherwise `exp(1 − reference /
candidate)` (3 places).

**Expected output:**

```
1.0
1.0
0.368
```
