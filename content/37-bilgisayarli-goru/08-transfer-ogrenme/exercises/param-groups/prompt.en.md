`group_summary(body_lr, head_lr)` should build a `torch.optim.Adam` with two
groups for the ready `body` and `head` (body `body_lr`, head `head_lr`) and
return a list of `[learning rate, parameter count]` for each group
(`optimizer.param_groups`).

**Expected output:**

```
[[0.0001, 80], [0.01, 27]]
```
