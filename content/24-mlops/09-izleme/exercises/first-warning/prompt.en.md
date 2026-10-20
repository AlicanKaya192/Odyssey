The monthly results of a few monitoring signals are in a dictionary: `{name: [fired in month 0?, fired in month 1?, ...]}`. Write the function `first_warning(signals)`:

- Find the **first** month in which any signal fired.
- Return `[month, the names of the signals that fired that month]`; the names in alphabetical order.
- If no signal ever fired, `None`.

The lists can have different lengths; if a signal's list has ended, it counts as not firing in those months.

**Expected output:**

```
[2, ['predicted_rate', 'usage_mean']]
None
```
