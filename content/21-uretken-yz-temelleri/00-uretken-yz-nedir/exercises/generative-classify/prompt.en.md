`classify(length, weight)` should find the fish's species the generative way.
For each species compute the mean and covariance from all fish, find the
species' share (`np.mean(y == name)`) and return the name of the species
with the larger `log_density(...) + np.log(share)` score. `log_density` is
given.

**Expected output:**

```
22 250 perch
33 620 bream
27 420 bream
29 380 perch
```
