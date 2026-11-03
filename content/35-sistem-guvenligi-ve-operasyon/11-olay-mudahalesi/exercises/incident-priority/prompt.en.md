`priority(impact, urgency)` should multiply impact and urgency (both 1–3):
return `"P1"` if the score is 6 or more, `"P2"` if 4 or more, otherwise
`"P3"`. If either is outside the range 1–3, return `"invalid"`: a
mistyped score must not silently turn into a priority.

**Expected output:**

```
P1
P1
P2
P3
invalid
```
