`g_loss(fake_logits)` should compute the generator's loss: for the logits the
discriminator gave the fakes, the target is **1** ("take me for real"),
`BCEWithLogitsLoss`. Return it with 3 places.

**Expected output:**

```
0.693
1.127
```
