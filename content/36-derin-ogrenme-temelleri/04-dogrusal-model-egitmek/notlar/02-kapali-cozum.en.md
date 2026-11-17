Linear regression has a **closed-form solution** that needs no gradient
descent: least squares. `LinearRegression` in the machine learning track
used it. In PyTorch it is `torch.linalg.lstsq`:

```python
A = torch.stack([x, torch.ones_like(x)], dim=1)
solution = torch.linalg.lstsq(A, y.unsqueeze(1)).solution
print(A.shape, [round(v, 2) for v in solution.flatten().tolist()])
```

```text
torch.Size([100, 2]) [2.99, 2.0]
```

- The first column of `A` is `x`, the second is all ones: the coefficient
  of the second column becomes the constant `b`.
- The result lands where the lesson's gradient descent did: `w ≈ 3`,
  `b ≈ 2`.

So why gradient descent? The closed form exists only for a linear model
with the mean squared error loss. As soon as a ReLU comes in between, there
is no formula; in deep learning the only way is to search step by step. We
picked a linear model in this section because we can compare what gradient
descent finds with the exact answer.
