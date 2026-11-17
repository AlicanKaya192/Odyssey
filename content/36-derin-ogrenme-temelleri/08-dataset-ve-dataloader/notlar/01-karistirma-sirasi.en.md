The order of shuffling comes from a random generator. If you fix the
generator with a seed, the same order repeats on every run:

```python
small = TensorDataset(torch.arange(10))
for seed in [0, 0, 1]:
    loader = DataLoader(small, batch_size=4, shuffle=True,
                        generator=torch.Generator().manual_seed(seed))
    print(seed, [b[0].tolist() for b in loader])
print("-", [b[0].tolist() for b in DataLoader(small, batch_size=4)])
```

```text
0 [[3, 7, 5, 2], [0, 8, 1, 6], [9, 4]]
0 [[3, 7, 5, 2], [0, 8, 1, 6], [9, 4]]
1 [[4, 6, 9, 2], [3, 1, 0, 7], [8, 5]]
- [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9]]
```

- The same seed (0, 0) gave the same order; another seed (1) another order.
- Without shuffling (`shuffle` not written, its default is `False`) the
  order is the data set's order.
- Even in a one-element `TensorDataset` each example is a tuple; hence
  `b[0]`.

The rule: `shuffle=True` (with a fixed generator) in the **training** loader,
`shuffle=False` in the **validation and test** loaders. The order does not
change an evaluation result, but a fixed order makes it easy to put
predictions next to labels and find the mistakes.
