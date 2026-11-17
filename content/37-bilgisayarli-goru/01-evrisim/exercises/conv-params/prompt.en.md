`conv_params(in_ch, out_ch, k)` should return the parameter count of an
`nn.Conv2d(in_ch, out_ch, k)` layer with biases, using a formula. The program
prints the result next to the layer's real count.

**Expected output:**

```
1 8 3 80 80
3 16 3 448 448
16 32 5 12832 12832
```
