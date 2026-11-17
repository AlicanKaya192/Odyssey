`receptive_field(layers)` should return the receptive field at the last layer
of a list of `[kernel, stride]` pairs. At the start the field is 1 and the
jump 1; at each layer the field grows by `(kernel - 1) * jump`, then the
jump is multiplied by the stride.

**Expected output:**

```
5
18
19
```
