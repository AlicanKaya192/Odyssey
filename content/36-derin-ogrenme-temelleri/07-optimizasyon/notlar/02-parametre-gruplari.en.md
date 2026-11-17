An optimizer's learning rate is not a fixed number; it is a setting in the
`param_groups` list that can be changed during training. Different layers
can also get different learning rates:

```python
model = nn.Sequential(nn.Linear(64, 32), nn.ReLU(), nn.Linear(32, 10))
optimizer = torch.optim.SGD([
    {"params": model[0].parameters(), "lr": 0.01},
    {"params": model[2].parameters()},
], lr=0.1)
print([group["lr"] for group in optimizer.param_groups])
for group in optimizer.param_groups:
    group["lr"] = group["lr"] / 2
print([group["lr"] for group in optimizer.param_groups])
```

```text
[0.01, 0.1]
[0.005, 0.05]
```

- Each group is a dictionary: `params` and optional settings. A group
  without a setting takes the default given to the optimizer (`lr=0.1`).
- Changing each group's `lr` in a loop is the plainest way to lower the
  learning rate during training. The schedulers in the Learning Rate
  Schedules section do exactly this inside.
- Different rates for different layers are common in transfer learning: a
  small learning rate for the pretrained layers, a large one for the new
  layer.
