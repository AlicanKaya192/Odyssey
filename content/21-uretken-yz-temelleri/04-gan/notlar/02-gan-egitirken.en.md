GAN training is delicate. In the section, raising only the learning rate from
0.002 to 0.01 lost two of the eight clusters with two of the three seeds.

**Checklist:**

1. **Look at what is generated.** A scatter plot for 2-dimensional data, a
   grid for images. The loss alone is not enough: in the section the
   collapsed run's final loss was slightly lower (1.380 healthy, 1.176
   collapsed), but it did not say which clusters had vanished.
2. **Count the kinds.** If the data has known groups (clusters, digits),
   count how many generated samples fall into each group. A group that gets
   no samples is a sign of mode collapse.
3. **Try a few seeds.** A single run can come out well or badly by chance; in
   the section the same setting gave eight clusters with one seed and six with
   two.
4. **Start with a small learning rate.** In the section 0.002 was safe.
   Adam's momentum coefficient is often 0.5 for GANs.
5. **Watch the discriminator.** At the end of training the mean probability
   it gives real and fake samples should be close to 0.5. If one goes to 1
   and the other to 0, the discriminator has won and the generator cannot
   learn.

**Common mistakes:**

- **Not taking the gradient from the discriminator's input in the generator's
  step.** The generator is updated with the gradient to the discriminator's
  input; the discriminator's own weight gradients are not used here.
- **Updating the discriminator in the generator's step too.** Each network
  changes only in its own step.
- **Taking the fake batch's label as 1 in the discriminator's step.** The
  logit gradient is `p` for fake and `p - 1` for real.
- **Using the old loss.** $\log(1 - D(G(z)))$ gives almost no gradient early
  on; use $-\log D(G(z))$.
