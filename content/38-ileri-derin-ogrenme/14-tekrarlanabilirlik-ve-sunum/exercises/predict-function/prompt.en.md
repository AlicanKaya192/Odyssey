The model is trained and built once. Write `predict(values)`:

- If there are not 6 values, `ValueError("expected 6 values, got N")`.
- The logits and a `softmax` inside `torch.inference_mode()`.
- Return `{"label": class name, "probability": its probability (2 places)}`.

**Expected output:**

```
high True
expected 6 values, got 1
```
