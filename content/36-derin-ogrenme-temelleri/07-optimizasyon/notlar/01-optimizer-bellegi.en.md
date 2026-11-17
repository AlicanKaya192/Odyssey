The values we called the "velocity" and the "averages" of momentum and Adam
are stored somewhere: in the optimizer's `state` dictionary, separately for
each parameter. Let us take one step and look at what they keep:

```python
for name, make in [("SGD", lambda p: torch.optim.SGD(p, lr=0.1)),
                   ("momentum", lambda p: torch.optim.SGD(p, lr=0.1, momentum=0.9)),
                   ("Adam", lambda p: torch.optim.Adam(p, lr=0.1))]:
    w = torch.zeros(1000, requires_grad=True)
    optimizer = make([w])
    (w - 1).pow(2).sum().backward()
    optimizer.step()
    state = optimizer.state[w]
    print(name, sorted(state), sum(v.numel() for v in state.values()))
```

```text
SGD [] 0
momentum ['momentum_buffer'] 1000
Adam ['exp_avg', 'exp_avg_sq', 'step'] 2001
```

- Plain SGD stores nothing.
- Momentum keeps one velocity per parameter (`momentum_buffer`): 1000
  parameters, 1000 more numbers.
- Adam keeps two averages (`exp_avg`, `exp_avg_sq`) and a step counter
  (`step`): extra memory twice the number of parameters.

For small models this does not matter. For a model with billions of
parameters, though, Adam's state takes more room than the model itself; the
memory budget of large models counts the optimizer state too. When saving a
model to continue training later, this state is saved as well (the Saving
section).
