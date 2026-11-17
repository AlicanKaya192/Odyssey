`d_loss(real_logits, fake_logits, smooth=1.0)` should compute the
discriminator's loss with `BCEWithLogitsLoss`: the real ones' target is
`smooth` (label smoothing), the fakes' target is 0; the **sum** of the two
terms. Return it with 3 places.

**Expected output:**

```
1.386
0.605
```
