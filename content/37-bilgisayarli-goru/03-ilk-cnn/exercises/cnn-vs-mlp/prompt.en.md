`train_and_test(make_model)` should build a model with the given function
(after `torch.manual_seed(0)`), train it as in the lesson (batch 32,
shuffling with `generator=torch.Generator().manual_seed(0)`, Adam
`lr=0.005`, 8 epochs) and return the test accuracy. The program compares the
CNN and the MLP with the same function.

**Expected output:**

```
True True
True
```
