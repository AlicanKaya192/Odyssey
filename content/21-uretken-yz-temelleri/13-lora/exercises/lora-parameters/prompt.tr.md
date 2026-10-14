`lora_params(d_in, d_out, r)` `d_in × d_out` boyutlu bir katman için üç değer
döndürsün: `[tam değişimin parametre sayısı, r ranklı LoRA'nın parametre
sayısı, LoRA'nın tama oranı]`. Tam `d_in * d_out`, LoRA `r * (d_in + d_out)`;
oran 4 basamağa yuvarlanmış `float`.

**Beklenen çıktı:**

```
[2048, 384, 0.1875]
[16777216, 65536, 0.0039]
```
