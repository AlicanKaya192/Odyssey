What if we stacked the block without residual connections and layer
normalisation, just putting attention and the feed-forward network one after
another? Let us try 16 layers with the lesson's weights; `Z` is the bare
stack, `R` the lesson's block:

```python
Z = R = X + Pe
for layer in range(1, 17):
    Z = np.maximum(multi_head(Z, mask) @ W1, 0) @ W2
    R = block(R, mask)
    if layer in [1, 2, 4, 8, 16]:
        sizes = [np.linalg.norm(M) for M in [Z, R, layer_norm(R)]]
        print(layer, " ".join(f"{s:.3f}" for s in sizes))
```

```text
1 5.191 16.942 8.944
2 2.703 25.603 8.944
4 0.835 46.354 8.944
8 0.037 89.631 8.944
16 0.000 171.878 8.944
```

The columns: the layer, the size of the bare stack, the size of the block and
the size of the block's normalised form.

- Without residual connections the signal shrinks at every layer and reaches
  zero in 16 layers: the top layer can see nothing of the input. In
  backpropagation the derivative goes the same way, so the lower layers
  cannot learn.
- With a residual connection each layer **adds** something to its input; the
  input always stays in place and the derivative goes straight down through
  the addition. This is the idea found in 2015 in image networks (ResNet)
  that made networks with hundreds of layers trainable.
- Because of the addition, the block's size grows across layers. Layer
  normalisation brings each sublayer's input to the same scale (the last
  column is always the same); that is why the arrangement with the norm at
  the input works stably in deep models.
