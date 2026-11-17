`nt_xent(z1, z2, tau)` should compute the lesson's loss: stack the two
groups, normalise, divide the similarity table by `tau`, set the diagonal to
`-inf`, then `F.cross_entropy` with the partners' positions. Return it with 3
places.

**Expected output:**

```
0.24
1.099
```
