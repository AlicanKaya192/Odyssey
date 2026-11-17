`lora_param_count(in_features, out_features, r)` iki sayıyı liste olarak
döndürsün: rank `r`'lik LoRA'nın eğittiği parametre sayısı
(`r · (giriş + çıkış)`) ve tam doğrusal katmanınki (ağırlık + sapma).

**Beklenen çıktı:**

```
[512, 4160]
[65536, 16781312]
```
