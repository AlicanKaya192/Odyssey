`CondNet` returns `x * 2` if the sum is positive and `x * -1` otherwise. As it
is, it uses an ordinary `if`, so exporting fails. Rewrite `forward` with
`torch.cond`; `cond_outputs` is ready.

**Expected output:**

```
[2.0, 4.0, 6.0]
[1.0, 2.0, -0.5]
```
