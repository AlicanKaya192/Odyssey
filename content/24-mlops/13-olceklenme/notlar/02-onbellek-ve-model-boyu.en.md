Two cheap ways to go faster: not computing the same question again, and
not using a bigger model than needed.

## The cache (50,000 requests, 6794 different customers)

| Cache size | Answered from the cache |
|---|---|
| 10 | 0.128 |
| 100 | 0.388 |
| 1000 | 0.667 |
| 5000 | 0.852 |

- **LRU:** when full, the one asked about least recently leaves.
- **Key:** customer + model version.
- **TTL:** every entry has a lifetime; when it runs out, it is computed
  again.

## Model size (random forest, depth 6)

| Trees | Accuracy |
|---|---|
| 5 | 0.810 |
| 20 | 0.812 |
| 100 | 0.813 |
| 400 | 0.814 |

On this computer a single prediction takes about 1 ms with 5 trees and
about 45 ms with 400.

## Don't

- Don't forget to put the model version in the cache key; a new model
  keeps showing the old scores.
- Don't multiply the latency by tens for a gain of a thousandth in
  accuracy; set a latency limit first.
