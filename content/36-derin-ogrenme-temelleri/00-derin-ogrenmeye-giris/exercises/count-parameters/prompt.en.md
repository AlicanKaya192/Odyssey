`count_parameters(sizes)` should return the number of parameters of a network
built with `nn.Linear` layers from a list of layer sizes (e.g. `[64, 32, 10]`). Each
consecutive `(input, output)` pair has `input * output` weights and `output`
constants.

**Expected output:**

```
2410
139
```
