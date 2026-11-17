`graph_ops(activation)` should export the ready model with the example
`torch.ones(2, 3)` and list, in order, the targets (`str(n.target)`) of the
graph's `call_function` nodes, with the leading `aten.` prefix removed.

**Expected output:**

```
['linear.default', 'relu.default', 'linear.default']
```
