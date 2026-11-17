`init_weights(module)` is called on every sub-module through `model.apply`. Only on
`nn.Linear` layers: initialise the weight with Kaiming (ReLU), zero the bias and
append the layer to the `visited` list. `init_report` returns `[number of layers
initialised, absolute sum of the biases]`.

**Expected output:**

```
[3, 0.0]
```
