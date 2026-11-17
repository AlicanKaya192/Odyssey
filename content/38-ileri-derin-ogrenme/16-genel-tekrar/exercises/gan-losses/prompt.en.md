`gan_losses(real_logits, fake_logits)` should compute both losses with
`BCEWithLogitsLoss`: the discriminator's (1 for the real ones, 0 for the fakes,
summed) and the generator's (1 for the fakes). Return a list with 3 places.

**Expected output:**

```
[1.386, 0.693]
```
