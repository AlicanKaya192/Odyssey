`n_per_group(p, mde, alpha=0.05, power=0.8)` should compute the users per
group for a two-rate test by formula:
2 · (z₁₋α/₂ + z_power)² · p(1 − p) / mde², rounded up. The starter code
uses a one-sided z.

**Expected output:**

```text
14128
```
