`crack_time(bits, guesses_per_second)` should give the average time to
find a random password in a readable form.

- The average time (seconds): `2 ** (bits - 1) / guesses_per_second`.
- Units from large to small: `"years"` (31,536,000 s), `"days"` (86,400),
  `"hours"` (3,600), `"minutes"` (60), `"seconds"` (1).
- Pick the first unit for which the time comes out **equal to or greater
  than 1** and return the tuple `(value, unit)`; `value` with
  `round(..., 1)`.
- If the time is shorter than a second too, the unit is `"seconds"`.

**Expected output:**

```
(1743.3, 'years')
(55.0, 'seconds')
(1.6, 'days')
(0.0, 'seconds')
```
