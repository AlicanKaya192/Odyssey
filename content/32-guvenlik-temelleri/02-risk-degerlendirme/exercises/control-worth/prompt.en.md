Write the function `control_worth(ale_before, ale_after, annual_cost)`.
Compute the control's net benefit (ALE before − ALE after − yearly cost),
round it with `round(..., 2)` and return the tuple `(net, worth_it)`: the
control is worth it if the net benefit is **greater than zero**.

**Expected output:**

```
(11000, True)
(-500, False)
```
