`generator_gets_grad(use_detach)` should backpropagate the discriminator's
loss (target 0 for the fake, `BCEWithLogitsLoss`) with the two small networks
built for you. If `use_detach` is true, detach the fake example first with
`detach()`. Return whether a derivative was written into the generator's
weight (`G.weight.grad is not None`).

**Expected output:**

```
False
True
```
