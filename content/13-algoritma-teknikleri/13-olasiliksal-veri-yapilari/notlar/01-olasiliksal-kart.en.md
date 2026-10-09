## Which structure for which question?

| Question | Structure | Exact counterpart |
|---|---|---|
| Has this item come before? | Bloom filter | `set` |
| How many times has it come? | Count-Min sketch | `Counter` / `dict` |
| How many distinct items came? | HyperLogLog | `len(set(...))` |
| How similar are two sets? | MinHash (+ LSH) | Jaccard, with the whole sets |

## Directions of error

- **Bloom:** false positives are possible, false negatives are not. It does not
  support deletion (resetting a bit deletes other items too).
- **Count-Min:** always overestimates; the relative error is large for rare
  items.
- **HyperLogLog:** can err in both directions; the error is about `1.04/√m`.
- **MinHash:** can err in both directions; as the signature length `k` grows,
  the error shrinks like `1/√k`.

## Mergeability

All of them are **mergeable**: two servers' Bloom filters merge with a bitwise
`or`, Count-Min tables with a cell-by-cell sum, HyperLogLog buckets with a
bucket-by-bucket `max`, MinHash signatures with a position-by-position `min`.
That is why in distributed systems each machine can keep its own summary and
merge them at the end.

## Common mistakes

- Using Python's `hash()`: for text it can change from run to run, and a saved
  filter is useless the next day. Use `hashlib`.
- Using one hash function `k` times: `k` different seeds are needed.
- Filling a Bloom filter with far more items than planned: the false positive
  rate climbs quickly; choose the size from the expected number of items up
  front.
