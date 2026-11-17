Test accuracy says **how good** the model is, not **whether it works
correctly**. Before delivery a few short checks, like unit tests in software,
catch silent mistakes. The code below uses the trained `model` from the
lesson.

```python
with torch.no_grad():
    probs = torch.softmax(model(x[test][:5]), dim=1)
    longer = model(torch.randn(3, 1, 128))
    alone = model(x[test][:1])
    together = model(x[test][:5])[:1]
    twice = torch.equal(model(x[test][:5]), model(x[test][:5]))
print(torch.allclose(probs.sum(dim=1), torch.ones(5)), tuple(longer.shape))
print(torch.allclose(alone, together, atol=1e-5), twice)
noise = 0.05 * torch.randn(x[test].shape, generator=torch.Generator().manual_seed(0))
stable = (predict(model, x[test] + noise) == predict(model, x[test])).float().mean()
print(stable.item() > 0.95)
```

```text
True (3, 2)
True True
True
```

Five checks, five questions:

- **Do the probabilities sum to 1?** Forgetting the softmax or taking it over
  the wrong dimension (`dim=0`) is caught here.
- **Does it work at another length?** A 128-measurement window also gave a
  `(3, 2)` output: thanks to `AdaptiveMaxPool1d`. A model expecting a fixed
  length would raise a shape error here.
- **Alone and in a batch, the same?** An example's answer must not depend on
  the examples next to it. If a `BatchNorm` is left in training mode, this
  check fails.
- **Two calls, the same?** If `eval()` is forgotten, dropout gives a different
  result on every call.
- **Robust to small noise?** A shake the size of measurement noise should not
  change most predictions. If it does, the model is making decisions on the
  edge.

These checks are a few lines and can be rerun after every training; putting
them into a test file with pytest, as in the Python Libraries: Advanced
module, is a natural next step.
