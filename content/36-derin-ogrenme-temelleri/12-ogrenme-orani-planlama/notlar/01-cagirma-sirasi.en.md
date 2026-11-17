If the scheduler's `step()` is called **before** the optimizer's, PyTorch
warns; the rate changes one epoch earlier than planned:

```python
import warnings

w = nn.Parameter(torch.zeros(1))
optimizer = torch.optim.SGD([w], lr=0.1)
scheduler = lr_scheduler.StepLR(optimizer, step_size=3)
with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    scheduler.step()
print(str(caught[0].message).split(". ")[0])
```

```text
Detected call of `lr_scheduler.step()` before `optimizer.step()`
```

- The right pattern: in every batch `zero_grad`, `backward`, (clipping if
  needed), `optimizer.step()`; once at the end of the epoch,
  `scheduler.step()`.
- Numbers such as `T_max` and `step_size` count **`scheduler.step()` calls**.
  If you call the scheduler in every batch (some warmup schedules do), you
  must give these numbers in steps, not epochs; otherwise the schedule ends in
  the first epoch.
- To read the rate for logging: `scheduler.get_last_lr()` or
  `optimizer.param_groups[0]["lr"]`.
