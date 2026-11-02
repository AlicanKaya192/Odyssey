Combine the Threat Modelling and Risk Assessment sections. Each threat
has the fields `id`, `stride`, `likelihood` (1–5) and `impact` (1–5).

`risk_register(threats)` should return a `[id, stride, score, level]` list
for every threat. Score = likelihood × impact; level 1–4 `"low"`, 5–9
`"medium"`, 10–16 `"high"`, 17–25 `"critical"`. Order: score from high to
low, ties by `id` in alphabetical order.

**Expected output:**

```
T0 E 20 critical
T1 S 20 critical
T3 D 9 medium
T2 I 8 medium
T4 R 2 low
```
