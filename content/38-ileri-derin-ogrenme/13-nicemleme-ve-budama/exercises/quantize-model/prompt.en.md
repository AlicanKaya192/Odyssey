The model is trained and `quantize` is ready. Quantise the weight of every
`nn.Linear` layer, add the `(q, scale)` pair to the `stored` list and replace
the weight with the restored value (`q.float() * scale`); do it all inside
`torch.no_grad()`. The last two lines print how many layers were stored, their
type, and whether the accuracy stayed close.

**Expected output:**

```
3 torch.int8
True
```
