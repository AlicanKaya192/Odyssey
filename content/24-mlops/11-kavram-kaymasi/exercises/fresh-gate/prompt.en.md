Write the function `fresh_gate(sets, now, max_age, min_gain)` that doesn't fall into the gate trap. `sets` are dictionaries with the keys `"month"`, `"old"` and `"new"` (the two models' accuracy on that set):

- Use only current sets: `now - month <= max_age`.
- If there is no current set, return `["no fresh set", 0]`.
- Gain = the mean of `new - old` over the current sets, rounded to three digits.
- If the gain is at least `min_gain`, return `["promote", gain]`, otherwise `["keep", gain]`.

**Expected output:**

```
['promote', 0.156]
['keep', -0.095]
['no fresh set', 0]
```
