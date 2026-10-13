Let us run the lesson's `train` function with three learning rates, three
epochs each:

```python
for lr in [0.01, 0.05, 0.1]:
    with np.errstate(all="ignore"):
        _, _, losses = train(lr=lr, epochs=3)
    print(lr, losses)
```

```text
0.01 [2.138, 1.5, 1.45]
0.05 [2.351, 1.835, 1.506]
0.1 [nan, nan, nan]
```

- At 0.1 the loss is `nan` (not a number) from the first epoch. The steps are
  so large that the dot products of the vectors grow and `exp` overflows
  (infinity); infinity minus infinity gives `nan`, and `nan` spreads through
  the whole table. A model that has become `nan` never recovers.
- `np.errstate(all="ignore")` silences NumPy's overflow warnings; we used it
  here to keep the output short. In real work, read the warning instead of
  silencing it: "overflow encountered in exp" signals a learning rate
  problem.
- On this small data 0.01 reached an even lower loss than 0.05 in three
  epochs. A larger rate does not always mean faster learning.

## In practice

- The learning rate is a setting; try a few values and look at the loss
  curve.
- The loss in the first epoch should be lower than the starting loss (every
  probability 0.5: `6 · log 2 ≈ 4.16`). If not, either the rate is too large
  or there is a derivative bug in the code.
- Word2Vec's own code also lowers the learning rate linearly during
  training: move fast at the start, fine-tune at the end.
