`train(steps, seed)` trains the lesson's noise predictor, but two lines are
missing in the loop. Build `xt` with the single formula:
`xt = np.sqrt(a) * x0 + np.sqrt(1 - a) * eps`; after running the network,
pass the loss gradient: `backward(acts, 2 * (acts[-1] - eps) / eps.size, net)`.
After training the function returns the prediction error on a separate check
batch. The network pieces are in the read-only `diffusion_base.py`.

**Expected output:**

```
0.386
```
