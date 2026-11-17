`trace_shapes(sizes, batch)` should pass an input of zeros through the layers of
the `build(sizes)` model one by one and, for every layer, append
`[the layer's class name, the output shape as a list]`.

**Expected output:**

```
['Linear', [3, 4]]
['ReLU', [3, 4]]
['Linear', [3, 2]]
```
