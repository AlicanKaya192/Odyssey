`sgns_loss(v, u_pos, u_negs)` should return the loss of one pair with 3
places:

`L = −log σ(v · u_pos) − Σ log σ(−v · u_k)`

`u_negs` is the list of negative context vectors. `sigmoid` is ready.

**Expected output:**

```
1.565
1.386
```
