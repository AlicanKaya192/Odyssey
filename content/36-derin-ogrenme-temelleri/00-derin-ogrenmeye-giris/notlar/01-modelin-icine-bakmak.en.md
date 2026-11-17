What is inside the lesson's model? `print(model)` lists the layers in
order; `named_parameters()` gives each parameter's name and shape:

```python
print(model)
for name, p in model.named_parameters():
    print(name, tuple(p.shape))
print(sum(p.numel() for p in model.parameters()))
```

```text
Sequential(
  (0): Linear(in_features=64, out_features=32, bias=True)
  (1): ReLU()
  (2): Linear(in_features=32, out_features=10, bias=True)
)
0.weight (32, 64)
0.bias (32,)
2.weight (10, 32)
2.bias (10,)
2410
```

- `0.weight` holds the weights of the first layer (position 0):
  `32 × 64`, that is, 64 weights for each output. `0.bias` has 32
  constants.
- ReLU (position 1) has no parameters; it does not appear in the list.
- `2.weight` is `10 × 32`, `2.bias` has 10 constants.
- In total `32·64 + 32 + 10·32 + 10` = 2410 numbers. Training
  adjusts every one of them. In large language and image models this
  number reaches billions; the idea is the same.

`p.numel()` is the number of elements in a tensor. A layer's weight shape
is written in `(output, input)` order; it looks reversed at first, but it
is always like this.
