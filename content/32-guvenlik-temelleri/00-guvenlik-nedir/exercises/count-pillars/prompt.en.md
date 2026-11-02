A week's incident log is a list of dictionaries: every incident has the
fields `leaked`, `modified` and `unreachable`.

Write the function `count_pillars(incidents)`: return the dictionary
`{"C": ..., "I": ..., "A": ...}`, with the number of incidents that broke
each leg. One incident can break more than one leg.

**Expected output:**

```
{'C': 2, 'I': 2, 'A': 3}
```
