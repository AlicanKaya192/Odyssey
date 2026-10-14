`train(steps, seed)` trains the lesson's GAN but the generator's step is
missing. After the discriminator's step write it: produce a fake batch from
new noise (`acts_g = forward(rng.normal(size=(128, 2)), gen)`), pass it
through the discriminator, call `backward` with the logit gradient
`(p_f - 1) / 128` and take the gradient to the input, call the generator's
`backward` with that gradient and update with `opt_g.step`. The function
returns the number of clusters found and the share of samples near a
cluster.

**Expected output:**

```
[8, 0.892]
```
