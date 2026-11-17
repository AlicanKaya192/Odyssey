If the loss suddenly becomes `nan` or `inf`, the rest of training is wasted:
`nan` turns every number it touches into `nan`. The most common cause is the
logarithm of zero:

```python
probs = torch.tensor([[1.0, 0.0], [0.5, 0.5]], requires_grad=True)
target = torch.tensor([1, 0])
loss = -probs[torch.arange(2), target].log().mean()
loss.backward()
print(loss.item(), torch.isfinite(probs.grad).all().item())

logits = torch.tensor([[10.0, -10.0]], requires_grad=True)
loss = nn.functional.cross_entropy(logits, torch.tensor([1]))
loss.backward()
print(round(loss.item(), 1), torch.isfinite(logits.grad).all().item())
```

```text
inf False
20.0 True
```

- Computing the loss by hand from probabilities produced `log 0 = −inf` when
  the true class got exactly 0, and the gradient broke.
- When `cross_entropy` computed the same "very sure and wrong" case from
  logits, it gave a large but finite loss; the gradient is finite too. It
  computes the logarithm together with the softmax, in a way that does not
  overflow. That is why `cross_entropy` or `log_softmax` is used instead of
  writing `log(softmax(...))` by hand.
- A one-line guard can go into the training loop:
  `if not torch.isfinite(loss): raise ValueError(...)`. The bug is then
  caught at the step where `nan` first appears.
- Other causes: a learning rate that is too large (divergence), unscaled
  input, division by zero. The gradient clipping and normalisation sections
  are about these.
