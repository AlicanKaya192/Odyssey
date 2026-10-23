`resolve(phrase, reference)` should resolve a phrase such as `"today at 9am"`,
`"tomorrow at 7pm"` or `"in 3 days at 10am"` against the reference time
`reference` (ISO text, e.g. `"2026-03-14T01:30:00+03:00"`):

- Case does not matter; the **whole** phrase must have this form, otherwise
  `"rejected"`.
- If there is no `am`/`pm`, `"needs_clarification"`.
- If the hour is not between 1 and 12, `"rejected"`. `12am` is midnight,
  `12pm` is noon.
- The result is `isoformat()` in the reference's time zone:
  `"2026-03-15T19:00:00+03:00"`.

**Expected output:**

```
2026-03-16T09:00:00+03:00
2026-03-15T00:00:00+03:00
needs_clarification
rejected
```
