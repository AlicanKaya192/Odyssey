`inference_flags()` should compute two outputs with the ready model: one
normal, one inside `torch.inference_mode()`. Return three values as a list:
the normal output's `requires_grad`, and the inference-mode output's
`requires_grad` and `is_inference()`.

**Expected output:**

```
[True, False, True]
```
