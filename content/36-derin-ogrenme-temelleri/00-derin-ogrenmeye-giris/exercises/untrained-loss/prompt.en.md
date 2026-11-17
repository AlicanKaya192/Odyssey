A model that gives every class the same score knows nothing. `untrained_loss(n_classes)`
should give scores of zeros for 4 examples (`torch.zeros(4, n_classes)`) and labels
of 0 to `nn.CrossEntropyLoss`, and return the loss with 3 places. Compare the
result with the lesson's first loss (2.33).

**Expected output:**

```
2.303
1.099
```
