BatchNorm uses the statistics of the **batch** in training. A batch of one
example has no standard deviation, so training mode raises an error;
evaluation mode uses the stored averages and works:

```python
bn = nn.BatchNorm1d(2)
one = torch.tensor([[1.0, 2.0]])
try:
    bn(one)
except ValueError as error:
    print(str(error).split(",")[0])
bn.eval()
print([round(v, 3) for v in bn(one)[0].tolist()])
```

```text
Expected more than 1 value per channel when training
[1.0, 2.0]
```

- A newly built layer has a stored mean of 0 and a variance of 1; in
  `eval()` the input passed through almost unchanged.
- That is why forgetting `model.eval()` when predicting with a BatchNorm
  model causes two problems: an error on a single example, and with several
  examples the result **depends on the other examples** in the batch (the
  same image gets different predictions in different batches).
- Very small batches (2–4 examples) in training also make BatchNorm
  unstable; if the batch size has to stay small, consider LayerNorm.
