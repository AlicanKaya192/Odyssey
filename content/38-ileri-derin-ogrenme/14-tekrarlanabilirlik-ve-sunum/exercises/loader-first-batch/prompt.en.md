`first_batch(seed)` should build a shuffling `DataLoader` over the numbers 0–9
with batches of 4 and return the first batch as a list. The shuffling order
must come from the seed: give the `DataLoader`
`torch.Generator().manual_seed(seed)`.

**Expected output:**

```
True
4
```
