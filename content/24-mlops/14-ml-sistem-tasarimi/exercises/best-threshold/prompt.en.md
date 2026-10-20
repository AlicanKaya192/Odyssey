Write the function `best_threshold(probs, labels, candidates, saved, cost)` that picks the threshold with the largest profit:

- For every threshold in `candidates`, compute the profit: `saved * label - cost` for every customer whose probability is at least the threshold.
- Pick the threshold giving the largest profit; on a tie, the one that comes first in the list.
- Return `[threshold, profit]`.

**Expected output:**

```
[0.3, 34]
[0.7, -1]
```
