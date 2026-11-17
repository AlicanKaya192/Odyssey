Weight decay is the gradient descent counterpart of adding the squares of
the weights to the loss (an L2 penalty): at every step a weight shrinks in
proportion to its own size. We can see this alone on a weight for which the
loss gives no gradient at all:

```python
w = torch.tensor([1.0], requires_grad=True)
optimizer = torch.optim.SGD([w], lr=0.1, weight_decay=0.1)
for _ in range(3):
    optimizer.zero_grad()
    (w * 0).sum().backward()
    optimizer.step()
    print(round(w.item(), 4))
```

```text
0.99
0.9801
0.9703
```

- The loss is `w · 0`, so its gradient is 0. Still, `w` drops to `1 − lr ·
  wd = 0.99` times itself at every step: 0.99, 0.9801, 0.9703.
- If the data does not really need a weight to be large, decay slowly takes
  it to zero. Large, odd weights coming from memorisation are worn down this
  way.
- In `Adam`, `weight_decay` is added to the gradient and goes through Adam's
  scaling, which spoils its effect; `AdamW` applies the decay separately.
  When you use Adam and want decay, choose `AdamW` (as we did in the lesson).
