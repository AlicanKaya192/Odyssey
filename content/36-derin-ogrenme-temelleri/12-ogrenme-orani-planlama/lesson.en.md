# Learning Rate Schedules and Gradient Clipping

So far the learning rate stayed fixed throughout training. A good training
run, however, often goes through two phases: approaching a good region
quickly with large steps at the start, and settling into it with small steps
at the end. A fixed, large rate makes the model bounce from side to side at
the bottom of the valley at the end; a fixed, small rate is slow from the
start. In this section we see **schedulers**, which change the rate during
training, and **gradient clipping**, which stops a single large gradient from
breaking the model.

## A scheduler: StepLR

A scheduler wraps an optimizer and changes its learning rate by a rule at
every `step()` call. The optimizer's current rate sits in
`optimizer.param_groups[0]["lr"]`. Schedulers live in the
`torch.optim.lr_scheduler` module. `StepLR` multiplies the rate by `gamma`
every `step_size` epochs:

```python
import torch
from torch import nn
from torch.optim import lr_scheduler

w = nn.Parameter(torch.zeros(1))
optimizer = torch.optim.SGD([w], lr=0.1)
scheduler = lr_scheduler.StepLR(optimizer, step_size=3, gamma=0.5)
rates = []
for epoch in range(8):
    rates.append(optimizer.param_groups[0]["lr"])
    optimizer.step()
    scheduler.step()
print(rates)
```

```text
[0.1, 0.1, 0.1, 0.05, 0.05, 0.05, 0.025, 0.025]
```

- 0.1 for the first three epochs, 0.05 for the next three, then 0.025: the
  rate goes down in steps.
- The order matters: first `optimizer.step()` (this epoch's step), then
  `scheduler.step()` (the next epoch's rate). There is no gradient here, so
  the step changes nothing; it is only there so we can watch the rates.

## A cosine schedule

`CosineAnnealingLR` lowers the rate to zero over `T_max` epochs without
steps, along a cosine curve: slowly at first, fast in the middle, slowly
again at the end.

```python
optimizer = torch.optim.SGD([w], lr=0.1)
scheduler = lr_scheduler.CosineAnnealingLR(optimizer, T_max=8)
rates = []
for epoch in range(9):
    rates.append(round(optimizer.param_groups[0]["lr"], 3))
    optimizer.step()
    scheduler.step()
print(rates)
```

```text
[0.1, 0.096, 0.085, 0.069, 0.05, 0.031, 0.015, 0.004, 0.0]
```

At the middle epoch (the 4th) the rate is exactly half, 0.05; at the 8th it
is zero. The formula: `lr · (1 + cos(π · epoch / T_max)) / 2`.

## Warmup

Sometimes the opposite is needed: at the very start of training the weights
are random, the gradients are erratic, and a large rate can break the model
in the first steps. **Warmup** starts the rate small and raises it to its
real value over a few epochs. `LinearLR` does this:

```python
optimizer = torch.optim.SGD([w], lr=0.1)
scheduler = lr_scheduler.LinearLR(optimizer, start_factor=0.25,
                                  total_iters=3)
rates = []
for epoch in range(6):
    rates.append(round(optimizer.param_groups[0]["lr"], 4))
    optimizer.step()
    scheduler.step()
print(rates)
```

```text
[0.025, 0.05, 0.075, 0.1, 0.1, 0.1]
```

The rate started at a quarter of 0.1, rose to 0.1 in three epochs and stayed
there. Large models often use warmup followed by a cosine schedule.

<figure class="fig">
  <div class="versus">
    <div><h5>StepLR</h5>Multiplies the rate by a fixed factor every few epochs; it goes down in steps.</div>
    <div><h5>CosineAnnealingLR</h5>Lowers the rate smoothly to zero along a cosine curve.</div>
    <div><h5>LinearLR (warmup)</h5>Starts the rate small and raises it to its real value over a few epochs.</div>
  </div>
  <figcaption>All three are used the same way: wrap the optimizer, call <code>scheduler.step()</code> at the end of every epoch.</figcaption>
</figure>

## The effect

Let us train a small network on the table data with a **large** rate (1.0)
for 60 epochs: once with a fixed rate, once with StepLR, once with cosine. At
the end of each run we print how much the training loss **wobbled** over the
last five epochs (largest − smallest) and the test accuracy:

```python
from dl_data import make_table

x_np, y_np = make_table(1000)
X, Y = torch.from_numpy(x_np), torch.from_numpy(y_np)
loss_fn = nn.CrossEntropyLoss()


def train(make_scheduler):
    torch.manual_seed(0)
    model = nn.Sequential(nn.Linear(6, 32), nn.ReLU(), nn.Linear(32, 3))
    optimizer = torch.optim.SGD(model.parameters(), lr=1.0)
    scheduler = make_scheduler(optimizer)
    generator = torch.Generator().manual_seed(0)
    history = []
    for epoch in range(60):
        order = torch.randperm(800, generator=generator)
        for start in range(0, 800, 32):
            idx = order[start:start + 32]
            optimizer.zero_grad()
            loss_fn(model(X[idx]), Y[idx]).backward()
            optimizer.step()
        if scheduler is not None:
            scheduler.step()
        with torch.no_grad():
            history.append(loss_fn(model(X[:800]), Y[:800]).item())
    with torch.no_grad():
        hits = model(X[800:]).argmax(dim=1) == Y[800:]
    accuracy = hits.float().mean().item()
    last = history[-5:]
    return round(max(last) - min(last), 2), round(100 * accuracy, 1)


schedules = {
    "constant": lambda opt: None,
    "step": lambda opt: lr_scheduler.StepLR(opt, 20, gamma=0.1),
    "cosine": lambda opt: lr_scheduler.CosineAnnealingLR(opt, 60),
}
for name, make in schedules.items():
    print(name, train(make))
```

```text
constant (0.05, 82.0)
step (0.0, 88.5)
cosine (0.0, 88.0)
```

- With the fixed rate the loss of the last epochs wobbles by
  0.05: the model cannot settle at the bottom, every epoch it
  bounces somewhere else. The test accuracy is 82.0%.
- In both schedules the rate got small at the end, so the loss settled (the
  wobble is close to zero) and the test accuracy was 88.5% and
  88.0%.
- This is the gain from changing only the **end**, with the same starting
  rate. A schedule gives the precision of a small rate at the end without
  giving up the speed of a large rate.

## Gradient clipping

Sometimes the gradient of one batch comes out huge: because of an unscaled
feature, an extreme example or a deep network. The optimizer takes a giant
step with that gradient and the model breaks at once. **Gradient clipping**
treats the gradients of all the parameters as a single vector; if the length
(norm) of that vector goes over a limit, it shortens the vector to that limit
without changing its direction:

```python
torch.manual_seed(0)
layer = nn.Linear(3, 1)
loss = (layer(torch.tensor([[100.0, 200.0, -50.0]])) - 1).pow(2).sum()
loss.backward()
norm = nn.utils.clip_grad_norm_(layer.parameters(), max_norm=1.0)
after = torch.sqrt(sum(p.grad.pow(2).sum() for p in layer.parameters()))
print(round(norm.item()), round(after.item(), 4))
```

```text
38423 1.0
```

- `clip_grad_norm_` returns the norm **before** clipping: 38423. After
  clipping the norm is exactly 1.
- Clipping goes between `backward()` and `optimizer.step()`: after the
  gradient is computed, before it is used.

To see its effect, let us learn the line `y = 3x + 2` with an unscaled
feature (between 0 and 100):

```python
import math

torch.manual_seed(0)
x = torch.rand(100, 1) * 100
y = 3 * x + 2
for clip in [None, 1.0]:
    torch.manual_seed(1)
    model = nn.Linear(1, 1)
    optimizer = torch.optim.SGD(model.parameters(), lr=0.01)
    for step in range(300):
        optimizer.zero_grad()
        ((model(x) - y) ** 2).mean().backward()
        if clip is not None:
            nn.utils.clip_grad_norm_(model.parameters(), max_norm=clip)
        optimizer.step()
    weight = model.weight.item()
    if math.isfinite(weight):
        weight = round(weight, 1)
    print(clip, weight)
```

```text
None nan
1.0 3.0
```

- Training without clipping diverged in the first steps and the weight
  became `nan`.
- With the same rate, clipped training brought the weight to 3. Every step is
  at most `lr · max_norm` long, so the model could not get out of control.
- Clipping does not replace scaling (the bias could not be fully learned in
  this time), but it is cheap insurance against an occasional large gradient.
  Recurrent networks (the advanced module) use it almost always.

## Summary

- A scheduler changes the optimizer's learning rate during training:
  `StepLR` in steps, `CosineAnnealingLR` smoothly, `LinearLR` for warmup.
- Order: `optimizer.step()`, then `scheduler.step()`.
- Starting with a large rate and shrinking it at the end lets the loss settle
  at the bottom.
- `nn.utils.clip_grad_norm_` limits the total norm of the gradients; it goes
  between `backward()` and `step()`.
