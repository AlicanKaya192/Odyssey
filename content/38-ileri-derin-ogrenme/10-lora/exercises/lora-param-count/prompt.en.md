`lora_param_count(in_features, out_features, r)` should return two numbers as
a list: the number of parameters a rank-`r` LoRA trains
(`r · (inputs + outputs)`) and that of the full linear layer (weight +
bias).

**Expected output:**

```
[512, 4160]
[65536, 16781312]
```
