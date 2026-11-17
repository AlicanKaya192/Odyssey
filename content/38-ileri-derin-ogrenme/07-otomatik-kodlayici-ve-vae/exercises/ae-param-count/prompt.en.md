`ae_param_count(code)` should build the lesson's autoencoder (encoder
`64 → 32 → code`, decoder `code → 32 → 64`, ReLU in between, a Sigmoid at the
end) and return the total parameter count of both parts.

**Expected output:**

```
4484
4354
```
