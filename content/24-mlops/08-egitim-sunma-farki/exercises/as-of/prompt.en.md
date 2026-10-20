A feature's history is a list sorted by date: every element is `[date, value]`, with dates as `"YYYY-MM-DD"`. Write the function `as_of(history, day)`: return the **last** value known on or before `day`.

- Values dated after `day` are ignored.
- If there is no value before `day` (or the list is empty), `None`.

**Expected output:**

```
1
4
None
None
```
