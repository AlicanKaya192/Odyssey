Complete the `LoRALinear` class: the parameters `A` (`r × inputs`, small
random numbers, `torch.randn(...) * 0.01`) and `B` (`outputs × r`, zeros) and
`scale = alpha / r`; `forward` should add `(x · Aᵀ · Bᵀ) · scale` to the base
output. `lora_report` is ready: is the output the base's at the start, how
many values are trained, does the output change once `B` is filled.

**Expected output:**

```
[True, 24, True]
```
