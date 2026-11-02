Every threat is a dictionary: `id`, `likelihood`, `impact`, `status`
(`"open"`, `"mitigated"` or `"accepted"`).

`next_to_fix(threats, n)` should return the ids of the `n` threats with the
highest score (likelihood × impact), taking **only open** (`"open"`)
threats. Threats with equal scores in alphabetical order of their ids.

**Expected output:**

```
['T1', 'T2']
['T1', 'T2', 'T4']
```
