`fit(transform)` should run the lesson's experiment: build the lesson CNN
after `torch.manual_seed(0)`, train it for 25 epochs with Adam (`lr=0.005`)
on `Shapes(x_small, y_small, transform)` with batch 16, shuffling with
`generator=torch.Generator().manual_seed(0)`; then return the accuracy on the
training pictures without augmentation and on the test pictures.

**Expected output:**

```
True
True
True
```
