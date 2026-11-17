In real use a model often receives a single image. Since the model is written
to work with batches, a batch dimension is added to the single image:
`(64,)` → `(1, 64)`. A small prediction function that does this:

```python
def predict(net, image):
    net.eval()
    with torch.no_grad():
        logits = net(image.unsqueeze(0))
    return logits.argmax(dim=1).item()


print([predict(fresh, X[i]) for i in test_idx[:8].tolist()])
print(Y[test_idx[:8]].tolist())

fresh.train()
try:
    fresh(X[test_idx[0]].unsqueeze(0))
except ValueError as error:
    print(str(error).split(",")[0])
```

```text
[2, 4, 8, 4, 9, 6, 8, 4]
[2, 4, 8, 4, 9, 6, 8, 7]
Expected more than 1 value per channel when training
```

- Seven of the first eight test images are right; the last one took a 7 for
  a 4.
- The function calls `net.eval()` itself. Without it BatchNorm would stay in
  training mode and fail on a single image: the last line is exactly that
  error (the note of the Initialisation and Normalisation section).
- `torch.no_grad()` turns off derivative tracking when predicting; it is both
  faster and lighter on memory.
