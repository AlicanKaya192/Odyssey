The data are numbers with mean -2 and standard deviation 0.5. The networks, the
optimisers and the start of the loop are ready. Write the two steps inside
the loop:

1. Discriminator: 1 for the real ones, 0 for `fake.detach()`; add the two
   losses, only `opt_d` takes a step.
2. Generator: target 1 for `D(fake)`; only `opt_g` takes a step.

The last two lines print whether the mean of the generated numbers is close
to -2 and the discriminator's average guess close to 0.5.

**Expected output:**

```
True
True
```
