The starter code holds the lesson's `train_lora`, but the gradients of `A` and
`B` were left at zero; LoRA learns nothing. For `M = W1 + A @ B`, `g_M` is
ready. Write the gradients: `g_A = g_M @ B.T`, `g_B = A.T @ g_M`.
`lora_accuracy(r)` returns the adapted network's accuracy on the new task.
The data and network functions are in the read-only `finetune_tools.py`.

**Expected output:**

```
0.94
```
