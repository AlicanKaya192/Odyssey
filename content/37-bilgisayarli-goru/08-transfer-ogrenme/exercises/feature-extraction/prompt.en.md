The source network was trained on shapes. `train_head(model, x, y)` should do
feature extraction: freeze the body (`model[0]`), give the optimizer (Adam,
`lr=0.005`) only the head, train for 20 epochs with batch 8 and
`generator=torch.Generator().manual_seed(0)`; in each epoch put the body into
`eval()` after `model.train()`. The program checks that the body's weight
**and** BatchNorm statistic did not change.

**Expected output:**

```
True
True
True
```
