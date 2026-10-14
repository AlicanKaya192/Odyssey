`lora_params(d_in, d_out, r)` should return three values for a layer of size
`d_in × d_out`: `[parameters of the full change, parameters of a rank-r
LoRA, LoRA's ratio to full]`. Full is `d_in * d_out`, LoRA
`r * (d_in + d_out)`; the ratio a `float` rounded to 4 places.

**Expected output:**

```
[2048, 384, 0.1875]
[16777216, 65536, 0.0039]
```
