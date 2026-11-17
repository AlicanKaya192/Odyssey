The network that looks for "3, 5" in a row in sequences and the data are ready.

1. Train for 20 epochs: shuffle every epoch with
   `torch.randperm(500, generator=gen)`, `cross_entropy` in batches of 50.
2. `model.eval()`; export it with the batch size freed by `torch.export.Dim`
   and save it to the file `detector.pt2`.

The ready code at the end loads the file and compares it with the golden
output.

**Expected output:**

```
True
True torch.Size([3, 2])
```
