`vote(answers)` should find the most frequent answer among those that are
not `None` (on a tie, the one that appears first in the list) and return
`[answer, number of votes, number of votes / number of all answers]`;
the share rounded to 2 places. If there is no valid answer,
`[None, 0, 0.0]`.

**Expected output:**

```
[193.41, 3, 0.6]
[None, 0, 0.0]
```
