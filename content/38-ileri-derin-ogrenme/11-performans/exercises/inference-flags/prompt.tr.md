`inference_flags()` hazır modelle iki çıkış hesaplasın: biri normal, biri
`torch.inference_mode()` içinde. Üç değeri liste olarak döndürsün: normal
çıkışın `requires_grad`'i, tahmin kipindeki çıkışın `requires_grad`'i ve
`is_inference()`'i.

**Beklenen çıktı:**

```
[True, False, True]
```
