`trainable_last(hidden)` should freeze all parameters of the network built for
you (`requires_grad_(False)`), open only the last layer again and return the
number of **trainable** parameters.

**Expected output:**

```
195
27
```
