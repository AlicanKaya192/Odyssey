`step_size(optimizer_class, scale)` takes a single step from `w = 1` on the loss
`scale · w²` and gives the size of the step. `first_step(scale)` should return
`[SGD step, Adam step]`. As the loss grows SGD's step grows; and Adam's?

**Expected output:**

```
0.01 [0.002, 0.1]
1.0 [0.2, 0.1]
100.0 [20.0, 0.1]
```
